import os

from app import app
from .lib import db
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

    query = flask.request.args.get('q')
    where_clause = None
    if query:
      pass
    summaries = transaction.query_songs(where_clause)
  songs = [{
      'title': summary.title,
      'path': os.path.join('/media', summary.path)
    } for summary in summaries]
  return flask.jsonify({'status': 'success', 'songs': songs}), 200
