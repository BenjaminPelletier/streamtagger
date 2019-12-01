import os
import re
import uuid

from app import app
from .lib import db
from .lib import tags
from . import player
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
  return flask.render_template('tags.html', tag_defs=tag_defs)


@app.route('/tags', methods=['POST'])
def post_tags():
  try:
    new_tag_name = flask.request.form['new_tag_name']
  except KeyError:
    return flask.jsonify({'status': 'error',
                          'message': 'Missing new_tag_name argument'}), 400
  for c in new_tag_name:
    if not re.search(r'[a-zA-Z0-9_.]', c):
      return flask.jsonify({'status': 'error',
                            'message': 'Invalid character in tag name: %s' % c}), 400
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


@app.route('/songs/<song_id>/tags/<tag_name>', methods=['POST'])
def post_tag(song_id, tag_name):
  song_id = uuid.UUID(song_id)
  try:
    tag_value = flask.request.form['tag_value']
    if tag_value == 'None':
      tag_value = None
    else:
      tag_value = int(tag_value)  #TODO: consider changing to double
  except KeyError:
    return flask.jsonify({'status': 'error',
                          'message': 'Missing tag_value argument'}), 400
  try:
    report_name = flask.request.form['report_name']
  except KeyError:
    return flask.jsonify({'status': 'error',
                          'message': 'Missing report_name argument'}), 400

  with db.transaction() as transaction:
    user_id, session_id = sessions.get_session(transaction)
    if user_id is None:
      return flask.redirect('/login')
    users = transaction.get_users()
    username = users[user_id]

    tagset = transaction.get_tags_for_song(song_id)
    tagdefs = transaction.get_tag_definitions()
    changes = False
    if tag_value is not None:
      if tag_name not in tagset or username not in tagset[tag_name] or tagset[tag_name][username].value != tag_value:
        tagset.add_label(tag_name, tagdefs[tag_name], username, tag_value)
        transaction.set_label(tagdefs[tag_name].id, song_id, user_id, tag_value)
        changes = True
    else:
      if tag_name in tagset and username in tagset[tag_name]:
        tagset.clear_label(tag_name, username)
        transaction.clear_label(tagdefs[tag_name].id, song_id, user_id)
        changes = True
    if changes:
      report = player.parse_reports(report_name, transaction)[0]
      tag_cell_html = player.make_tag_cell(report, tag_value, username)
      #summary = transaction.get_song_by_id(song_id)
      #song_details = song.SongDetails(os.path.join(config.media_path, summary.path))
      #song_details.tags = tagset
      #song_details.save()
      transaction.commit()
      return flask.jsonify({'status': 'success',
                            'data_changed': True,
                            'tag_cell_html': tag_cell_html}), 200

  return flask.jsonify({'status': 'success', 'data_changed': False}), 200

# Tag colors
# 1b1b5b
# 5d29b0
# d63a49
# e58603
# e5d14b
