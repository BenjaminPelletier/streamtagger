import collections

from .lib import db
from .lib.flaskapp import app
from .lib import jinja
from . import sessions

import flask


Report = collections.namedtuple('Report', ('name', 'tag_name', 'username', 'tag_type'))


def make_tag_cell(report, value, username):
  editable = report.username is None or report.username == username
  if value is None:
    if editable:
      icon_class = ['editable_tag face_unselected'] * 5
    else:
      # This is a report of someone else's value of a tag; user can't edit
      return ''
  else:
    if report.tag_type == 'faces':
      tag_class = 'editable_tag ' if editable else ''
      icon_class = [(tag_class + ('face%d_selected' % i if t0 <= value < t1 else 'face_unselected'))
                    for t0, t1, i in ((1, 1.5, 1), (1.5, 2.5, 2), (2.5, 3.5, 3), (3.5, 4.5, 4), (4.5, 5.0001, 5))]
    else:
      icon_class = None
  tag_cell_template = jinja.env.get_template('tag_cell.html')
  return tag_cell_template.render(tag_type=report.tag_type, icon_class=icon_class)


def make_table(songs, username, tagsets=None, reports=None):
  if not tagsets:
    tagsets = {}
  if not reports:
    reports = []
  header = ['Title', 'Artist', 'Added']
  header.extend(r.name for r in reports)
  song_rows = []
  song_ids = [song.song_id for song in songs]
  song_paths = ['/media/' + song.path for song in songs]
  for i, song in enumerate(songs):
    cols = []
    cols.append(('col_title', song.title if song.title else ''))
    cols.append(('col_artist', song.artist if song.artist else ''))
    cols.append(('moment-relative', song.added_at))
    tagset = tagsets.get(song.song_id)
    for report in reports:
      value = tagset.compute_report_value(report) if tagset else None
      cols.append(make_tag_cell(report, value, username))
    song_rows.append(cols)
  table_template = jinja.env.get_template('song_table.html')
  return table_template.render(header=header, song_rows=song_rows, song_ids=song_ids, song_paths=song_paths)


def render_player(songs, users, username, tagsets=None, reports=None):
  table_html = make_table(songs, username, tagsets, reports)
  player = jinja.env.get_template('player.html')
  return player.render(initial_song_table=table_html, username=username)


def parse_reports(report_str, transaction):
  reports = []
  if not report_str:
    return reports
  tagdefs = transaction.get_tag_definitions()
  for report_name in report_str.split(','):
    if '@' in report_name:
      username, tag_name = report_name.split('@')
    else:
      username, tag_name = None, report_name
    reports.append(Report(name=report_name, tag_name=tag_name, username=username, tag_type=tagdefs[tag_name].type))
  return reports


@app.route('/', methods=['GET'])
def index():
  with db.transaction() as transaction:
    user_id, session_id = sessions.get_session(transaction)
    if user_id is None:
      return flask.redirect('/login')
    users = transaction.get_users()
    username = users[user_id]
    songs = transaction.query_songs('')
    tagsets, tag_names = transaction.get_tags([song.song_id for song in songs])
    reports = parse_reports(flask.request.args.get('show'), transaction)
  return render_player(songs, users, username, tagsets, reports)
