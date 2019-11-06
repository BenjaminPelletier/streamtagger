from .lib import config
from .lib import db
from .lib.flaskapp import app
from .lib import jinja
from . import sessions

import flask

def make_table(songs, username, tagsets=None, report_names=None):
  if not tagsets:
    tagsets = {}
  if not report_names:
    report_names = []
  header = ['Title', 'Artist', 'Added']
  header.extend(report_names)
  song_rows = []
  song_ids = [song.song_id for song in songs]
  song_paths = ['/media/' + song.path for song in songs]
  for i, song in enumerate(songs):
    cols = []
    cols.append(('col_title', song.title if song.title else ''))
    cols.append(('col_artist', song.artist if song.artist else ''))
    cols.append(('moment-relative', song.added_at))
    tagset = tagsets.get(song.song_id)
    if tagset:
      for report_name in report_names:
        value = tagset.make_report(report_name)
        if value:
          cols.append(str(value))
        else:
          cols.append('')
    else:
      cols.extend([''] * len(report_names))
    song_rows.append(cols)
  table_template = jinja.env.get_template('song_table.html')
  return table_template.render(header=header, song_rows=song_rows, song_ids=song_ids, song_paths=song_paths)


def render_player(songs, users, username, tagsets=None, tag_names=None):
  table_html = make_table(songs, username, tagsets, tag_names)
  player = jinja.env.get_template('player.html')
  return player.render(initial_song_table=table_html, username=username)


@app.route('/', methods=['GET'])
def index():
  show_reports = flask.request.args.get('show')
  if show_reports:
    show_reports = show_reports.split(',')
  with db.transaction() as transaction:
    user_id, session_id = sessions.get_session(transaction)
    if user_id is None:
      return flask.redirect('/login')
    users = transaction.get_users()
    username = users[user_id]
    songs = transaction.query_songs('')
    tagsets, tag_names = transaction.get_tags([song.song_id for song in songs])
  return render_player(songs, users, username, tagsets, show_reports)
