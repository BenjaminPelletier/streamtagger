import os

from app import app
from .lib import db
from .lib import query
from . import sessions

import flask
import flask_login


@app.route('/playlists/<playlistname>', methods=['GET'])
@flask_login.login_required
def playlist(playlistname):
  with db.transaction() as transaction:
    users = transaction.get_users()

    userids_by_name = {v: k for k, v in users.items()}
    where_clauses = query.get_where_clauses(flask.request.args, transaction,
                                            userids_by_name)
    summaries = transaction.query_songs(where_clauses)
    base_path = flask.request.args.get('basepath', '/')

    if playlistname[-4:].lower() == '.m3u':
      lines = ['#EXTM3U'] + [base_path + '/' + summary.path
                             for summary in summaries]
      return flask.Response(
        response='\n'.join(lines),
        status=200,
        mimetype='audio/x-mpegurl')
    else:
      return flask.Response(
        response='Unsupported extension: ' + playlistname[-4:].lower(),
        status=400)
