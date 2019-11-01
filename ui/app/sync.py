import datetime
import glob
import os
import threading
import uuid

from .lib import config
from .lib import db
from .lib.flaskapp import app
from .lib import jinja
from .lib import jobs
from .lib import song
from . import librarian
from . import sessions

import flask

ADMIN_USERS = {'admin', 'ben'}
sync_job_lock = threading.Lock()
sync_jobs = {}


@app.route('/sync', methods=['GET'])
def get_sync():
  with db.transaction() as transaction:
    user_id, session_id = sessions.get_session(transaction)
    if user_id is None:
      return flask.redirect('/login')
    users = transaction.get_users()
    username = users[user_id]
    if username not in ADMIN_USERS:
      return flask.jsonify({'status': 'error',
                            'message': 'User %s not authorized to perform this action' % username}), 403

  with sync_job_lock:
    for job_id, job in sync_jobs.items():
      if job.is_active():
        return flask.redirect('/sync/' + next(sync_jobs.keys()))

  sync_template = jinja.env.get_template('sync.html')
  return sync_template.render(logs=None, job_id=datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S'))


@app.route('/sync/<job_id>', methods=['GET'])
def get_sync_progress(job_id):
  with db.transaction() as transaction:
    user_id, session_id = sessions.get_session(transaction)
    if user_id is None:
      return flask.redirect('/login')
    users = transaction.get_users()
    username = users[user_id]
    if username not in ADMIN_USERS:
      return flask.jsonify({'status': 'error',
                            'message': 'User %s not authorized to perform this action' % username}), 403

  with sync_job_lock:
    if job_id not in sync_jobs:
      return flask.jsonify({'status': 'error',
                            'message': 'Job ID %s not found' % job_id}), 404

    progress_template = jinja.env.get_template('job_progress.html')
    return progress_template.render(logs=sync_jobs[job_id].get_logs())


@app.route('/sync/<job_id>', methods=['POST'])
def post_sync_start(job_id):
  with db.transaction() as transaction:
    user_id, session_id = sessions.get_session(transaction)
    if user_id is None:
      return flask.redirect('/login')
    users = transaction.get_users()
    username = users[user_id]
  if username not in ADMIN_USERS:
    return flask.jsonify({'status': 'error',
                          'message': 'User %s not authorized to perform this action' % username}), 403
  with sync_job_lock:
    sync_job = jobs.Job()
    sync_jobs[job_id] = sync_job
  sync_job.start(sync)
  return flask.redirect('/sync/' + job_id)


def sync(job):
  file_song_ids = sync_songs_from_folder(config.media_path, job)
  print(file_song_ids)
  #TODO: remove songs in DB but not on disk


def sync_songs_from_folder(path, job):
  job.log('Syncing folder %s' % path)
  with db.transaction() as transaction:
    users = {username: user_id for user_id, username in transaction.get_users().items()}
    song_ids = []
    for mp3_filename in glob.glob(os.path.join(path, '*.mp3')):
      song_ids.append(sync_song(mp3_filename, users, transaction, job))
    if song_ids:
      job.log('Committing database changes...')
      transaction.commit()

  for subfolder in (f.path for f in os.scandir(path) if f.is_dir()):
    song_ids.extend(sync_songs_from_folder(subfolder, job))
  return song_ids


def sync_song(mp3_filename, users, transaction, job):
  song_details = song.SongDetails(mp3_filename)
  media_path = os.path.relpath(mp3_filename, config.media_path)
  song_id = transaction.get_song_id(media_path)
  if song_details.song_id and not song_id:
    # No database entry for the song at this path.  See if there is a DB entry for song ID
    songs = transaction.get_songs_by_ids([song_details.song_id])
    if songs:
      song_id = song_details.song_id

  if song_id:
    # Song exists in database
    songs = transaction.get_songs_by_ids([song_id])
    summary = songs[0]

    # Update file, if necessary
    if (song_details.song_id != summary.song_id or
        song_details.added_by != summary.added_by or
        song_details.added_at != summary.added_at):
      song_details.song_id = song_details.song_id if song_details.song_id else summary.song_id
      song_details.added_by = song_details.added_by if song_details.added_by else summary.added_by
      song_details.added_at = song_details.added_at if song_details.added_at else summary.added_at
      job.log('Updating song file: %s' % media_path)
      song_details.save()
    else:
      job.log('Song file already up to date: %s' % media_path)

    # Update database from file, if necessary
    summary, to_update = song_details.make_summary(media_path, summary)
    if to_update:
      transaction.update_song(summary)
      job.log('Updating database: %s %s' % (media_path, ', '.join('%s: %s -> %s' % u for u in to_update)))
  else:
    # Song does not yet exist in database
    job.log('Adding song not in database: %s' % media_path)

    song_details.song_id = transaction.add_song(
      song_id=song_details.song_id,
      path=media_path,
      title=song_details.title,
      artist=song_details.artist,
      user_id=users.get(song_details.added_by),
      username=song_details.added_by,
      added_at=song_details.added_at)

  return song_id
