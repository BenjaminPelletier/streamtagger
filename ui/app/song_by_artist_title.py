import uuid

from app import app
from .lib import db
from . import sessions
from . import player
from .lib import query

import flask
import flask_login


@app.route('/songs/<artist>/<song_title>', methods=['GET'])
@flask_login.login_required
def songs_by_artist_title(artist, song_title):
  with db.transaction() as transaction:
    users = transaction.get_users()

    userids_by_name = {v: k for k, v in users.items()}
    where_clauses = query.get_where_clauses(flask.request.args, transaction,
                                            userids_by_name)

    artist = artist.lower()
    song_title = song_title.lower()
    if where_clauses:
      songs = transaction.query_songs(where_clauses)
      songs = [song for song in songs
               if artist in song.artist.lower()
               and song_title in song.title.lower()]
    else:
      songs = transaction.find_songs_by_artist_title(artist, song_title)
    if len(songs) == 0:
      return flask.jsonify({'status': 'error',
                            'message': 'No songs found with artist %s and title %s' % (artist, song_title)}), 404
    return player.render_player(songs=songs, transaction=transaction, show=flask.request.args.get('show'))


@app.route('/songs/<request_id>', methods=['GET'])
@flask_login.login_required
def songs_by_id(request_id):
  with db.transaction() as transaction:
    users = transaction.get_users()

    # See if the user is asking for a specific song ID
    try:
      song_id = uuid.UUID(request_id)
      song_id = str(song_id)
    except ValueError:
      song_id = None

    if song_id:
      songs = transaction.get_songs_by_ids([song_id])
      song = songs[0]
      return flask.render_template(
        'song_by_artist_title.html',
        song_title=song.get_title(),
        song_artist=song.get_artist(),
        song_id=song.song_id,
        song_path='/media/' + song.path)

    userids_by_name = {v: k for k, v in users.items()}
    where_clauses = query.get_where_clauses(flask.request.args, transaction,
                                            userids_by_name)

    request_id = request_id.lower()
    if where_clauses:
      songs = transaction.query_songs(where_clauses)
      songs_for_artist = [song for song in songs if song.artist is not None and request_id in song.artist.lower()]
      songs_for_title = [song for song in songs if song.title is not None and request_id in song.title.lower()]
    else:
      songs_for_artist = transaction.find_songs_by_artist_title(request_id, '')
      songs_for_title = transaction.find_songs_by_artist_title('', request_id)
    songs = songs_for_artist if len(songs_for_artist) >= len(songs_for_title) else songs_for_title

    if len(songs) == 0:
      return flask.jsonify({'status': 'error',
                            'message': 'No songs found with artist, title, or ID "%s"' % request_id}), 404
    return player.render_player(songs=songs, transaction=transaction, show=flask.request.args.get('show'))
