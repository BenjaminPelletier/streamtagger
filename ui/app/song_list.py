import os

from app import app
from .lib import db
from .lib import query
from . import sessions

import flask


@app.route('/song_list', methods=['GET'])
def song_list():
  with db.transaction() as transaction:
    user_id, session_id = sessions.get_session(transaction)
    if user_id is None:
      return flask.jsonify({'status': 'error', 'message': 'No valid user signed in'}), 401
    users = transaction.get_users()
    username = users[user_id]

    userids_by_name = {v: k for k, v in users.items()}
    where_clauses = query.get_where_clauses(flask.request.args, transaction, userids_by_name)
    summaries = transaction.query_songs(where_clauses)
  songs = [{
      'title': summary.title,
      'path': '/media/' + summary.path
    } for summary in summaries]
  return flask.jsonify({'status': 'success', 'songs': songs}), 200
