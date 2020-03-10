import datetime
import uuid

import flask

from app import app
from app.models import User
from .lib import db


import flask_login
from werkzeug.urls import url_parse


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
  if flask_login.current_user.is_authenticated:
    return flask.redirect(flask.url_for('index', **flask.request.args))

  return flask.render_template('login.html')


def login_post():
  username = flask.request.form['username']
  password_hash = flask.request.form['password_hash']
  if not flask_login.current_user.is_authenticated:
    user = User.query.filter(User.username==username).first()
    if user is None or not user.check_password(password_hash):
      return flask.jsonify({
        'success': False,
        'message': 'Invalid username or password'
      })
    flask_login.login_user(user, remember=True)
    with db.transaction() as transaction:
      ip = flask.request.environ.get('HTTP_X_REAL_IP',
                                     flask.request.environ['REMOTE_ADDR'])
      session_id = transaction.add_session(user.id, ip)
      transaction.commit()

  next_page = flask.request.args.get('next')
  args_minus_next = {k: v for (k, v) in flask.request.args.items()}
  if not next_page or url_parse(next_page).netloc != '':
    next_page = flask.url_for('index', **args_minus_next)

  resp = flask.make_response(flask.jsonify({
    'success': True,
    'redirect': next_page
  }))
  resp.set_cookie(SESSION_KEY, session_id)
  return resp


@app.route('/login', methods=['GET', 'POST'])
def login():
  if flask.request.method == 'GET':
    return login_get()
  if flask.request.method == 'POST':
    return login_post()


@app.route('/logout')
def logout():
  flask_login.logout_user()
  return flask.redirect(flask.url_for('login'))
