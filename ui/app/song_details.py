import uuid

from .lib import db
from .lib.flaskapp import app
from .lib import jinja
from . import librarian
from . import sessions
from . import player

import flask


@app.route('/song_details/<song_id>', methods=['GET'])
def get_song_details(song_id):
  with db.transaction() as transaction:
    user_id, session_id = sessions.get_session(transaction)
    if user_id is None:
      return flask.redirect('/login')
    users = transaction.get_users()
    username = users[user_id]
    songs = transaction.get_songs_by_ids([song_id])
    # TODO: get tags from MP3 here for consistency check with DB
  if len(songs) == 0:
    return flask.jsonify({'status': 'error',
                          'message': 'No song found with ID %s' % song_id}), 404
  song = songs[0]

  details_template = jinja.env.get_template('song_details.html')
  exclude_attribute_keys = {song.get_artist_key(), song.get_title_key()}
  exclude_attribute_keys = exclude_attribute_keys.union(librarian.READONLY_TAGS)
  return details_template.render(
    song_id=song_id,
    song_title=song.get_title(),
    song_title_key=song.get_title_key(),
    song_artist=song.get_artist(),
    song_artist_key=song.get_artist_key(use_default=True),
    song_tags=', '.join(str(k) if v is None else '%s:%s' % (k, v) for (k, v) in song.tags.items()),
    song_attributes = {k: v for k, v in song.attributes.items() if k not in exclude_attribute_keys}
  )

@app.route('/song_details/<song_id>', methods=['POST'])
def post_song_details(song_id):
  with db.transaction() as transaction:
    user_id, session_id = sessions.get_session(transaction)
    if user_id is None:
      return flask.redirect('/login')
    users = transaction.get_users()
    username = users[user_id]
    songs = transaction.get_songs_by_ids([song_id])

    if len(songs) == 0:
      return flask.jsonify({'status': 'error',
                            'message': 'No song found with ID %s' % song_id}), 404
    song = songs[0]
    new_attributes = {k: flask.request.form[k] for k in song.changed_attributes(flask.request.form)}
    transaction.update_song_attributes(song_id, new_attributes)
    transaction.commit()

  return flask.jsonify({'status': 'success'}), 200
