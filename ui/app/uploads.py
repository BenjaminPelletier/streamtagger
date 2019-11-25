import datetime
import os
import subprocess
import uuid

from .lib import config
from .lib import db
from .lib.flaskapp import app
from .lib import jinja
from .lib import song
from . import sessions

import flask


def is_unsafe_filename(filename):
  return any(c in '\\/*:?"<>|\0' for c in filename)


def upload_error(message):
  return flask.jsonify({'status': 'error', 'message': message}), 400


@app.route('/upload', methods=['GET'])
def get_upload():
  with db.transaction() as transaction:
    user_id, session_id = sessions.get_session(transaction)
    if user_id is None:
      return flask.jsonify({'message': 'You must be logged in to upload files'}), 401
  upload_template = jinja.env.get_template('upload.html')
  return upload_template.render()


@app.route('/upload', methods=['POST'])
def post_upload():
  with db.transaction() as transaction:
    user_id, session_id = sessions.get_session(transaction)
    if user_id is None:
      return flask.jsonify({'message': 'You must be logged in to upload files'}), 401

  if 'file' not in flask.request.files:
    return upload_error('No file specified in upload request')
  if len(flask.request.files) == 0:
    return upload_error('No files included in upload request')
  if len(flask.request.files) > 1:
    return upload_error('Only one file allowed per upload request')
  file = next(flask.request.files.values())
  if is_unsafe_filename(file.filename):
    return upload_error('Illegal characters in filename')
  extension = file.filename[-4:].lower()
  approved_extensions = {'.mp3', '.m4a'}
  if extension not in approved_extensions:
    return upload_error('Only %s files may be uploaded' % ', '.join(approved_extensions))
  approved_content_types = {'audio/mp3', 'audio/x-m4a'}
  if file.content_type not in approved_content_types:
    return upload_error('Only %s content may be uploaded' % ', '.join(approved_content_types))

  dest_path = datetime.datetime.now().strftime('%Y%m')
  local_dest_path = config.media_path + '/' + dest_path
  if not os.path.exists(local_dest_path):
    os.mkdir(local_dest_path)

  dest_filename = dest_path + '/' + file.filename

  local_dest_filename = config.media_path + '/' + dest_filename
  file.save(local_dest_filename)

  if file.content_type == 'audio/x-m4a':
    mp3_dest_filename = dest_filename[:-4] + '.mp3'
    mp3_local_dest_filename = local_dest_filename[:-4] + '.mp3'
    args = ['ffmpeg', '-y', '-i', local_dest_filename, '-b:a', '192k', mp3_local_dest_filename]
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env={'PATH': os.getenv('PATH')})
    try:
      outs, errs = proc.communicate(timeout=60)
    except subprocess.TimeoutExpired:
      proc.kill()
      outs, errs = proc.communicate()
    os.remove(local_dest_filename)
    if proc.returncode != 0:
      return upload_error('Error converting %s to mp3: %s' % (dest_filename, errs))
    dest_filename = mp3_dest_filename
    local_dest_filename = mp3_local_dest_filename

  song_details = song.SongDetails(local_dest_filename)

  with db.transaction() as transaction:
    song_id = transaction.get_song_id(dest_filename)
    if song_id:
      # Song with this filename already exists
      old_summary = transaction.get_songs_by_ids([song_id])[0]
      summary, to_update = song_details.make_summary(dest_filename, old_summary)
      transaction.update_song(summary)
    else:
      # Song is new
      users = transaction.get_users()
      username = users[user_id]
      transaction.add_song(
        path=dest_filename,
        title=song_details.title,
        artist=song_details.artist,
        user_id=user_id,
        username=username)

    remote_dest_filename = '/media/' + dest_filename
    transaction.commit()
    return flask.jsonify({'status': 'ok', 'path': remote_dest_filename})


@app.route('/songs/<song_id>', methods=['DELETE'])
def delete_song(song_id):
  try:
    song_id = uuid.UUID(song_id)
  except ValueError as e:
    return flask.jsonify({'status': 'error',
                          'message': 'Did not recognize song_id as valid ID: ' + str(e)})

  with db.transaction() as transaction:
    user_id, session_id = sessions.get_session(transaction)
    if user_id is None:
      return flask.jsonify({'message': 'You must be logged in to delete files'}), 401
    song_summaries = transaction.get_songs_by_ids([song_id])
    if len(song_summaries) == 0:
      return flask.jsonify({'status': 'error',
                            'message': 'No song found with ID %s' % song_id}), 404
    song_summary = song_summaries[0]

    transaction.delete_song(song_id)

    os.remove(config.media_path + '/' + song_summary.path)
    transaction.commit()

  return flask.jsonify({'status': 'ok', 'deleted': song_id})
