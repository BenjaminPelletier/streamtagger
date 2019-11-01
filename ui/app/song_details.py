import uuid

from .lib import config
from .lib import db
from .lib.flaskapp import app
from .lib import jinja
from .lib import song
from . import librarian
from . import sessions

import flask
import mutagen.easyid3
import mutagen.id3


@app.route('/song_details/<song_id>', methods=['GET'])
def get_song_details(song_id):
  try:
    song_id = uuid.UUID(song_id)
  except ValueError as e:
    return flask.jsonify({'status': 'error',
                          'message': 'Did not recognize song_id as valid ID: ' + str(e)})

  with db.transaction() as transaction:
    user_id, session_id = sessions.get_session(transaction)
    if user_id is None:
      return flask.redirect('/login')
    users = transaction.get_users()
    username = users[user_id]
    song_summaries = transaction.get_songs_by_ids([song_id])
  if len(song_summaries) == 0:
    return flask.jsonify({'status': 'error',
                          'message': 'No song found with ID %s' % song_id}), 404
  song_summary = song_summaries[0]

  tag_types = {} #TODO: populate tag_types correctly

  # Read MP3 file as ground truth
  label_entries = song.SongDetails(config.media_path + song_summary.path).tags.get_user_label_entries(username)
  try:
    id3 = mutagen.easyid3.EasyID3(config.media_path + song_summary.path)
  except mutagen.id3.ID3NoHeaderError:
    id3 = mutagen.easyid3.EasyID3()
  if 'title' not in id3:
    id3['title'] = [song_summary.title]

  song_attributes = []
  preferred_order = ('title', 'artist', 'albumartist', 'album')
  for key in preferred_order:
    if key in id3:
      song_attributes.append((key, id3[key][0]))
      del id3[key]
    else:
      song_attributes.append((key, ''))
  for key, values in id3.items():
    song_attributes.append((key, values[0]))  #TODO: decide what to do with multi-valued keys

  details_template = jinja.env.get_template('song_details.html')
  return details_template.render(
    song_id=song_id,
    song_path=song_summary.path,
    song_tags=', '.join(label_entries),
    song_attributes=song_attributes
  )

@app.route('/song_details/<song_id>', methods=['POST'])
def post_song_details(song_id):
  with db.transaction() as transaction:
    user_id, session_id = sessions.get_session(transaction)
    if user_id is None:
      return flask.redirect('/login')
    users = transaction.get_users()
    username = users[user_id]
    song_summaries = transaction.get_songs_by_ids([song_id])

    if len(song_summaries) == 0:
      return flask.jsonify({'status': 'error',
                            'message': 'No song found with ID %s' % song_id}), 404
    summary = song_summaries[0]

    # Update attributes, if necessary
    try:
      id3 = mutagen.easyid3.EasyID3(config.media_path + summary.path)
    except mutagen.id3.ID3NoHeaderError:
      id3 = mutagen.easyid3.EasyID3()

    changes = False
    for k, v in flask.request.form.items():
      if k == 'tags':
        continue  # TODO: process tags

      if not v:
        # User blanked tag value
        if (k in id3) and id3[k][v]:
          # Tag in file is not blanked; remove it
          del id3[k]
          changes = True
        else:
          # No tag in file, or it's already blank; no change
          continue

      if k in id3:
        # Tag already exists in file
        if id3[k][0] == v:
          # No change to tag value
          continue

      # Add or update tag value
      id3[k] = [v]
      changes = True

    if changes:
      id3.save(config.media_path + summary.path, v2_version=3)

    song_details = song.SongDetails(config.media_path + summary.path)
    summary, to_update = song_details.make_summary(summary.path, summary)
    if to_update:
      transaction.update_song(summary)
      transaction.commit()

  return flask.jsonify({'status': 'success', 'updates': {u[0]: u[2] for u in to_update}}), 200
