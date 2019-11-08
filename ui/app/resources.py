import os

from .lib import config
from .lib import db
from .lib.flaskapp import app
from . import sessions

import flask


@app.route('/favicon.ico', methods=['GET'])
def favicon():
 return flask.send_file('../../static/favicon.ico', mimetype='image/x-icon')


@app.route('/static/<path:path>', methods=['GET'])
def static_content(path):
  return flask.send_file('../../static/' + path)


@app.route('/media/<path:path>', methods=['GET'])
def media(path):
  with db.transaction() as transaction:
    user_id, session_id = sessions.get_session(transaction)
    if user_id is None:
      return flask.jsonify({'message': 'You must be logged in to access media'}), 401

  return flask.send_file(os.path.join(config.media_path, path), mimetype='audio/mpeg')
