import datetime
import uuid

import flask

from app import app
from .lib import db


SESSION_KEY = 'streamtagger_session'

SESSION_TIMEOUT = datetime.timedelta(hours=24)


def get_session(transaction):
  try:
    session_id = uuid.UUID(flask.request.cookies.get(SESSION_KEY, None)).hex
  except (ValueError, TypeError):
    return None, None
  if session_id:
    username, last_used = transaction.get_session(session_id)
    if username:
      if SESSION_TIMEOUT is None or datetime.datetime.utcnow() < last_used + SESSION_TIMEOUT:
        return username, session_id
  return None, None


def login_get():
  with db.transaction() as transaction:
    user_id, session_id = get_session(transaction)
    if user_id:
      # User already logged in with valid session
      return flask.redirect(flask.url_for('index', **flask.request.args))

  return flask.render_template('login.html')


def login_post():
  username = flask.request.form['username']
  password_hash = flask.request.form['password_hash']
  with db.transaction() as transaction:
    user_id, db_password_hash = transaction.get_user(username)
    if not user_id:
      return flask.jsonify({
        'success': False,
        'message': 'Unknown user ' + username
      })

    if db_password_hash != password_hash:
      return flask.jsonify({
        'success': False,
        'message': 'Supplied password does not match database'
      })

    ip = flask.request.environ.get('HTTP_X_REAL_IP', flask.request.environ['REMOTE_ADDR'])
    session_id = transaction.add_session(user_id, ip)
    transaction.commit()

  resp = flask.make_response(flask.jsonify({
    'success': True,
    'redirect': flask.url_for('index', **flask.request.args)
  }))
  resp.set_cookie(SESSION_KEY, session_id)
  return resp


@app.route('/login', methods=['GET', 'POST'])
def login():
  if flask.request.method == 'GET':
    return login_get()
  if flask.request.method == 'POST':
    return login_post()
