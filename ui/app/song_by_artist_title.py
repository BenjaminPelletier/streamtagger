import uuid

from .lib import config
from .lib import db
from .lib.flaskapp import app
from .lib import jinja
from . import sessions
from . import player

import flask

def render_songs(songs, users, username):
  if len(songs) == 1:
    song = songs[0]
    song_template = jinja.env.get_template('song_by_artist_title.html')
    return song_template.render(song_title=song.get_title(),
                                song_artist=song.get_artist(),
                                song_id=song.song_id,
                                song_path='/media/' + song.path,
                                username=username)
  else:
    return player.render_player(songs=songs, users=users, username=username)

@app.route('/<artist>/<song_title>', methods=['GET'])
def songs_by_artist_title(artist, song_title):
  with db.transaction() as transaction:
    user_id, session_id = sessions.get_session(transaction)
    if user_id is None:
      return flask.redirect('/login')
    users = transaction.get_users()
    username = users[user_id]
    songs = transaction.find_songs_by_artist_title(artist, song_title)
  if len(songs) == 0:
    return flask.jsonify({'status': 'error',
                          'message': 'No songs found with artist %s and title %s' % (artist, song_title)}), 404
  return render_songs(songs, users, username)


@app.route('/<request_id>', methods=['GET'])
def songs_by_id(request_id):
  with db.transaction() as transaction:
    user_id, session_id = sessions.get_session(transaction)
    if user_id is None:
      return flask.redirect('/login')
    users = transaction.get_users()
    username = users[user_id]

    try:
      song_id = uuid.UUID(request_id)
      song_id = str(song_id)
    except ValueError:
      song_id = None

    if song_id:
      songs = transaction.get_songs_by_ids([song_id])
      song = songs[0]
      song_template = jinja.env.get_template('song_by_artist_title.html')
      return song_template.render(song_title=song.get_title(),
                                  song_artist=song.get_artist(),
                                  song_id=song.song_id,
                                  song_path='/media/' + song.path,
                                  username=username)

    songs_for_artist = transaction.find_songs_by_artist_title(request_id, '')
    songs_for_title = transaction.find_songs_by_artist_title('', request_id)
    songs = songs_for_artist if len(songs_for_artist) >= len(songs_for_title) else songs_for_title

    if len(songs) == 0:
      return flask.jsonify({'status': 'error',
                            'message': 'No songs found with artist, title, or ID "%s"' % request_id}), 404
    return render_songs(songs, users, username)
