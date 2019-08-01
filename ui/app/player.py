from .lib import config
from .lib import db
from .lib.flaskapp import app
from .lib import jinja
from . import sessions

import flask

print('player imported')
def make_table(transaction, users):
  songs = transaction.query_songs('')

  header = ('Title', 'Artist')
  song_rows = []
  song_ids = [song.song_id for song in songs]
  song_paths = ['media/' + song.path for song in songs]
  for i, song in enumerate(songs):
    cols = []
    cols.append(song.get_title())
    cols.append(song.get_artist())
    song_rows.append(cols)
  table_template = jinja.env.get_template('song_table.html')
  return table_template.render(header=header, song_rows=song_rows, song_ids=song_ids, song_paths=song_paths)


@app.route('/', methods=['GET'])
def index():
  print('index requested', flush=True)
  with db.transaction() as transaction:
    user_id, session_id = sessions.get_session(transaction)
    if user_id is None:
      return flask.redirect('/login')
    users = transaction.get_users()
    username = users[user_id]
    table_html = make_table(transaction, users)
  player = jinja.env.get_template('player.html')
  return player.render(initial_song_table=table_html, username=username)
