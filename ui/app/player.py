import collections

from app import app

from .lib import db
from .lib import query
from . import sessions

import flask
import flask_login


Report = collections.namedtuple('Report', ('name', 'tag_name', 'username', 'tag_type'))


def make_tag_cell(report, value):
  editable = report.username is None or report.username == flask_login.current_user.username
  return flask.render_template(
    'tag_cell.html',
    tag_type=report.tag_type, tag_name=report.tag_name, tag_value=value, editable=editable, report_name=report.name)


def make_table(songs, tagsets=None, reports=None):
  if not tagsets:
    tagsets = {}
  if not reports:
    reports = []
  header = ['Title', 'Artist', 'Added']
  header.extend(('tag_header', r.name) for r in reports)
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
      cols.append(make_tag_cell(report, value))
    song_rows.append(cols)
  return flask.render_template(
    'song_table.html',
    header=header, song_rows=song_rows, song_ids=song_ids, song_paths=song_paths)


def render_player(songs, transaction, show=None):
  tagsets, tag_names = transaction.get_tags([song.song_id for song in songs])
  reports = parse_reports(show, transaction)
  table_html = make_table(songs, tagsets, reports)
  return flask.render_template('player.html', initial_song_table=table_html)


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
@app.route('/songs', methods=['GET'])
@flask_login.login_required
def index():
  with db.transaction() as transaction:
    users = transaction.get_users()

    userids_by_name = {v: k for k, v in users.items()}
    where_clauses = query.get_where_clauses(flask.request.args, transaction, userids_by_name)

    songs = transaction.query_songs(where_clauses)
    return render_player(songs=songs, transaction=transaction, show=flask.request.args.get('show'))
