from .lib import db
from .lib.flaskapp import app
from .lib import jinja
from .lib import tags
from . import sessions

import flask


@app.route('/tags', methods=['GET'])
def get_tags():
  with db.transaction() as transaction:
    user_id, session_id = sessions.get_session(transaction)
    if user_id is None:
      return flask.redirect('/login')
    users = transaction.get_users()
    username = users[user_id]
    tag_defs = transaction.get_tag_definitions()
  tags_template = jinja.env.get_template('tags.html')
  return tags_template.render(tag_defs=tag_defs)


@app.route('/tags', methods=['POST'])
def post_tags():
  try:
    new_tag_name = flask.request.form['new_tag_name']
  except KeyError:
    return flask.jsonify({'status': 'error',
                          'message': 'Missing new_tag_name argument'}), 400
  try:
    new_tag_type = flask.request.form['new_tag_type']
  except KeyError:
    return flask.jsonify({'status': 'error',
                          'message': 'Missing new_tag_type argument'}), 400
  if new_tag_type not in tags.Tag.TYPES:
    return flask.jsonify({'status': 'error',
                          'message': 'Invalid tag type: %s' % new_tag_type}), 400

  with db.transaction() as transaction:
    user_id, session_id = sessions.get_session(transaction)
    if user_id is None:
      return flask.redirect('/login')
    users = transaction.get_users()
    username = users[user_id]
    tag_defs = transaction.get_tag_definitions()
    if new_tag_name in tag_defs:
      return flask.jsonify({'status': 'error',
                            'message': 'Tag named %s already exists' % new_tag_name}), 409
    tag_def_id = transaction.create_tag_definition(new_tag_name, new_tag_type, user_id)
    transaction.commit()

  return flask.jsonify({'status': 'success', 'tag_def_id': str(tag_def_id)}), 200
