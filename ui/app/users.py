from .lib import config
from .lib import db
from .lib.flaskapp import app
from .lib import jinja
from . import sessions

import flask


def user_post(logged_in_username, username, users, transaction):
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


@app.route('/users/<username>', methods=['GET', 'POST'])
def user_page(username):
  with db.transaction() as transaction:
    user_id, session_id = sessions.get_session(transaction)
    if user_id is None:
      return flask.redirect('/login')
    users = transaction.get_users()
    logged_in_username = users[user_id]
    if flask.request.method == 'POST':
      return user_post(logged_in_username, username, users, transaction)
  if username != logged_in_username:
    return flask.redirect('/users/' + logged_in_username)
  template = jinja.env.get_template('user.html')
  return template.render(username=username)
