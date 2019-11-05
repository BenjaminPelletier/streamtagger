import datetime
import os

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
  if file.filename[-4:].lower() != '.mp3':
    return upload_error('Only .mp3 files may be uploaded')
  if file.content_type != 'audio/mp3':
    return upload_error('Only mp3 content may be uploaded')

  dest_path = datetime.datetime.now().strftime('%Y%m')
  local_dest_path = os.path.join(config.media_path, dest_path)
  if not os.path.exists(local_dest_path):
    os.mkdir(local_dest_path)

  dest_filename = os.path.join(dest_path, file.filename)

  local_dest_filename = os.path.join(config.media_path, dest_filename)
  file.save(local_dest_filename)

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
