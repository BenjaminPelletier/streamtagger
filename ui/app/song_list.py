import os

from app import app
from .lib import db
from .lib import query
from . import sessions

import flask
import flask_login


@app.route('/song_list', methods=['GET'])
@flask_login.login_required
def song_list():
  with db.transaction() as transaction:
    users = transaction.get_users()

    userids_by_name = {v: k for k, v in users.items()}
    where_clauses = query.get_where_clauses(flask.request.args, transaction, userids_by_name)
    summaries = transaction.query_songs(where_clauses)
    songs = [{
        'title': summary.title,
        'path': '/media/' + summary.path
      } for summary in summaries]
    return flask.jsonify({'status': 'success', 'songs': songs}), 200
