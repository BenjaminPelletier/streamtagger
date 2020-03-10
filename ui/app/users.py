from app import app
from .lib import db
from . import sessions

import flask
import flask_login


@app.route('/users/<username>', methods=['POST'])
@flask_login.login_required
def post_user(username):
  with db.transaction() as transaction:
    user_id, session_id = sessions.get_session(transaction)
    users = transaction.get_users()
    logged_in_username = users[user_id]
    if logged_in_username != 'admin':
      return flask.jsonify({'status': 'error', 'message': 'Only admin may add users'}), 403
    if 'password_hash' not in flask.request.form:
      return flask.jsonify({'status': 'error', 'message': 'Password hash missing'}), 403
    password_hash = flask.request.form['password_hash']
    if username in users.values():
      transaction.update_user_with_hash(username, password_hash)
      user_id = {v: k for k, v in users.items()}[username]
    else:
      user_id = transaction.add_user_with_hash(username, password_hash)
    transaction.commit()
  return flask.jsonify({'status': 'success', 'user_id': user_id})


@app.route('/users/<username>', methods=['GET'])
@flask_login.login_required
def get_user(username):
  if username != flask_login.current_user.username:
    return flask.redirect('/users/' + flask_login.current_user.username)
  return flask.render_template('user.html')
