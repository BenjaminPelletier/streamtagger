import uuid

from .lib import db
from .lib.flaskapp import app
from .lib import jinja
from . import sessions
from . import player

import flask


@app.route('/song_details/<song_id>', methods=['GET'])
def ajax_get_song_details(song_id):
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

  details_template = jinja.env.get_template('song_details.html')
  return details_template.render(
    song_id=song_id,
    song_title=song.get_title(),
    song_artist=song.get_artist(),
    song_tags=', '.join(str(k) if v is None else '%s:%s' % (k, v) for (k, v) in song.tags.items())
  )

@app.route('/song_details/<song_id>', methods=['POST'])
def ajax_post_song_details(song_id):
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
  return flask.jsonify({'status': 'success'}), 200
