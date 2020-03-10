import os

from app import app

from .lib.config import Config

import flask
import flask_login


@app.route('/favicon.ico', methods=['GET'])
def favicon():
 return flask.send_file('static/favicon.ico', mimetype='image/x-icon')


@app.route('/static/<path:path>', methods=['GET'])
def static_content(path):
  return flask.send_file('static/' + path)


@app.route('/media/<path:path>', methods=['GET'])
@flask_login.login_required
def media(path):
  return flask.send_file(os.path.join(Config.media_path, path), mimetype='audio/mpeg')
