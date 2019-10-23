import datetime
import hashlib
import os
import threading

from .song import Song

import psycopg2

# https://www.iconfinder.com/iconsets/media-cartoony

PASSWORD_SALT = 'K80Tgi^w1&jc'

_connection = psycopg2.connect(os.environ.get('ST_DB_CONNECTIONSTRING'))
_transaction_lock = threading.Lock()


def transaction():
  return Transaction(_connection)


class Transaction(object):
  def __init__(self, connection):
    self._connection = connection
    self._committed = False

  def __enter__(self):
    _transaction_lock.acquire()
    self._cursor = self._connection.cursor()
    return self

  def commit(self):
    self._connection.commit()
    self._committed = True

  def __exit__(self, type, value, traceback):
    if not self._committed:
      self._connection.rollback()
    _transaction_lock.release()

  def clear_database(self):
    SQL_CLEAR_DATABASE = """
      DROP TABLE IF EXISTS
        attributes,
        tags,
        tag_definitions,
        songs,
        sessions,
        users;
    """

    self._cursor.execute(SQL_CLEAR_DATABASE)

  def init_database(self):
    SQL_ENABLE_CRYPTO = """
      CREATE EXTENSION IF NOT EXISTS "pgcrypto";
    """

    SQL_CREATE_USERS_TABLE = """
      CREATE TABLE IF NOT EXISTS users (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        username VARCHAR NOT NULL UNIQUE,
        password_hash VARCHAR NOT NULL
      );
    """

    SQL_CREATE_SESSIONS_TABLE = """
      CREATE TABLE IF NOT EXISTS sessions (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        user_id UUID NOT NULL REFERENCES users (id) ON DELETE CASCADE,
        created_at TIMESTAMP NOT NULL,
        created_ip VARCHAR NOT NULL,
        last_used TIMESTAMP NOT NULL
      );
    """

    SQL_CREATE_SONGS_TABLE = """
      CREATE TABLE IF NOT EXISTS songs (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        path VARCHAR NOT NULL UNIQUE,
        added TIMESTAMP NOT NULL,
        added_with UUID REFERENCES sessions (id) ON DELETE RESTRICT
      );
    """

    SQL_CREATE_TAG_DEFINITIONS_TABLE = """
      CREATE TABLE IF NOT EXISTS tag_definitions (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        name VARCHAR NOT NULL UNIQUE,
        created_by UUID REFERENCES users (id) ON DELETE RESTRICT,
        created_at TIMESTAMP NOT NULL
      );
    """

    SQL_CREATE_TAGS_TABLE = """
      CREATE TABLE IF NOT EXISTS tags (
        tag_id UUID NOT NULL REFERENCES tag_definitions (id) ON DELETE CASCADE,
        song_id UUID NOT NULL REFERENCES songs (id) ON DELETE CASCADE,
        user_id UUID NOT NULL REFERENCES users (id) ON DELETE CASCADE,
        value INT NOT NULL,
        last_changed TIMESTAMP NOT NULL,
        PRIMARY KEY (tag_id, song_id, user_id)
      );
    """

    SQL_CREATE_ATTRIBUTES_TABLE = """
      CREATE TABLE IF NOT EXISTS attributes (
        song_id UUID NOT NULL REFERENCES songs (id) ON DELETE CASCADE,
        name VARCHAR NOT NULL,
        value VARCHAR NOT NULL,
        PRIMARY KEY (song_id, name)
      );
    """

    self._cursor.execute(SQL_ENABLE_CRYPTO)
    self._cursor.execute(SQL_CREATE_USERS_TABLE)
    self._cursor.execute(SQL_CREATE_SESSIONS_TABLE)
    self._cursor.execute(SQL_CREATE_SONGS_TABLE)
    self._cursor.execute(SQL_CREATE_TAG_DEFINITIONS_TABLE)
    self._cursor.execute(SQL_CREATE_TAGS_TABLE)
    self._cursor.execute(SQL_CREATE_ATTRIBUTES_TABLE)

  def add_user(self, username, password):
    SQL_INSERT_USER = """
      INSERT INTO users
      (username, password_hash) VALUES (%s, %s)
      RETURNING id;
    """
    salted_password = (PASSWORD_SALT + password + PASSWORD_SALT).encode('ascii', 'backslashreplace')
    password_hash = hashlib.sha1(salted_password).hexdigest()
    self._cursor.execute(SQL_INSERT_USER, [username, password_hash])
    row = self._cursor.fetchone()
    user_id = row[0]
    return user_id

  def add_user_with_hash(self, username, password_hash):
    SQL_INSERT_USER = """
      INSERT INTO users
      (username, password_hash) VALUES (%s, %s)
      RETURNING id;
    """

    self._cursor.execute(SQL_INSERT_USER, [username, password_hash])
    row = self._cursor.fetchone()
    user_id = row[0]
    return user_id

  def update_user_with_hash(self, username, password_hash):
    SQL_UPDATE_USER = """
      UPDATE users
      SET password_hash = %s
      WHERE username = %s;
    """

    self._cursor.execute(SQL_UPDATE_USER, [password_hash, username])

  def get_user(self, username):
    SQL_SELECT_USER_BY_USERNAME = """
      SELECT id, password_hash
      FROM users
      WHERE username=%s
    """
    self._cursor.execute(SQL_SELECT_USER_BY_USERNAME, [username])
    row = self._cursor.fetchone()
    if row:
      return row
    else:
      return None, None

  def get_users(self):
    SQL_SELECT_USERS = """
      SELECT id, username
      FROM users;
    """
    self._cursor.execute(SQL_SELECT_USERS)
    return {row[0]: row[1] for row in self._cursor.fetchall()}

  def add_session(self, user_id, ip):
    SQL_INSERT_SESSION = """
      INSERT INTO sessions
      (user_id, created_at, created_ip, last_used) VALUES (%s, %s, %s, %s)
      RETURNING id;
    """
    timestamp = datetime.datetime.utcnow().isoformat()
    self._cursor.execute(SQL_INSERT_SESSION, [user_id, timestamp, ip, timestamp])
    row = self._cursor.fetchone()
    session_id = row[0]
    return session_id

  def get_session(self, session_id):
    SQL_SELECT_SESSION = """
      SELECT user_id, last_used
      FROM sessions
      WHERE id=%s
    """
    self._cursor.execute(SQL_SELECT_SESSION, [session_id])
    row = self._cursor.fetchone()
    if row:
      user_id = row[0]
      last_used = row[1]
      return user_id, last_used
    else:
      return None, None

  def add_song(self, path, session_id):
    SQL_INSERT_SONG = """
      INSERT INTO songs
      (path, added, added_with) VALUES (%s, %s, %s)
      RETURNING id;
    """
    timestamp = datetime.datetime.utcnow().isoformat()
    self._cursor.execute(SQL_INSERT_SONG, [path, timestamp, session_id])
    row = self._cursor.fetchone()
    song_id = row[0]
    return song_id

  def update_song(self, song_id, path, session_id):
    SQL_UPDATE_SONG = """
      UPDATE songs
      SET (path, added, added_with) = (%s, %s, %s)
      WHERE id = %s;
    """
    timestamp = datetime.datetime.utcnow().isoformat()
    self._cursor.execute(SQL_UPDATE_SONG, [path, timestamp, session_id, song_id])

  def get_tag_ids(self, tags, user_id):
    ids = {}
    SQL_FIND_TAGS = """
      SELECT id, name
      FROM tag_definitions
      WHERE name IN %s
    """
    self._cursor.execute(SQL_FIND_TAGS, (tags,))
    for row in self._cursor.fetchall():
      ids[row[1]] = row[0]

    SQL_DEFINE_TAG = """
      INSERT INTO tag_definitions
      (name, created_by, created_at) VALUES (%s, %s, %s)
      RETURNING id;
    """
    timestamp = datetime.datetime.utcnow().isoformat()
    for tag in set(tags) - set(ids):
      self._cursor.execute(SQL_DEFINE_TAG, (tag, user_id, timestamp))
      row = self._cursor.fetchone()
      ids[tag] = row[0]

    return ids

  def get_tag_id(self, tag, user_id):
    SQL_FIND_TAG = """
      SELECT id
      FROM tag_definitions
      WHERE name LIKE %s
    """
    self._cursor.execute(SQL_FIND_TAG, (tag,))
    row = self._cursor.fetchone()
    if row:
      return row[0]

    SQL_DEFINE_TAG = """
      INSERT INTO tag_definitions
      (name, created_by, created_at) VALUES (%s, %s, %s)
      RETURNING id;
    """
    timestamp = datetime.datetime.utcnow().isoformat()
    self._cursor.execute(SQL_DEFINE_TAG, (tag, user_id, timestamp))
    row = self._cursor.fetchone()
    return row[0]

  def set_tag(self, tag_def_id, song_id, user_id, value):
    SQL_UPSERT_TAG = """
      INSERT INTO tags
      (tag_id, song_id, user_id, value, last_changed) VALUES (%s, %s, %s, %s, %s)
      ON CONFLICT (tag_id, song_id, user_id) DO
      UPDATE SET (value, last_changed) = (EXCLUDED.value, EXCLUDED.last_changed);
    """
    timestamp = datetime.datetime.utcnow().isoformat()
    self._cursor.execute(SQL_UPSERT_TAG, [tag_def_id, song_id, user_id, value, timestamp])

  def clear_tag(self, tag_def_id, song_id, user_id):
    SQL_REMOVE_TAG = """
      DELETE FROM tags
      WHERE tag_id = %s AND song_id = %s AND user_id = %s;
    """
    self._cursor.execute(SQL_REMOVE_TAG, [tag_def_id, song_id, user_id])

  def get_song_id(self, path):
    SQL_GET_SONG = """
      SELECT id FROM songs
      WHERE path LIKE %s;
    """
    self._cursor.execute(SQL_GET_SONG, [path])
    row = self._cursor.fetchone()
    if row:
      song_id = row[0]
      return song_id
    else:
      return None

  def query_songs(self, query):
    SQL_SELECT_SONGS = """
      SELECT songs.id, songs.path, songs.added, users.username
      FROM songs as songs
      JOIN sessions as sessions ON songs.added_with = sessions.id
      JOIN users as users ON sessions.user_id = users.id
      ORDER BY songs.added DESC
      LIMIT 200;
    """
    songs = []
    self._cursor.execute(SQL_SELECT_SONGS)
    for row in self._cursor.fetchall():
      song_id = row[0]
      attributes = self.get_song_attributes(song_id)
      tags = self.get_tags(song_id)
      songs.append(Song(song_id, row[1], row[2], row[3], attributes, tags))
    return songs

  def get_song_attributes(self, song_id):
    SQL_SELECT_ATTRIBUTES = """
      SELECT name, value
      FROM attributes
      WHERE song_id = %s;
    """
    attributes = {}
    self._cursor.execute(SQL_SELECT_ATTRIBUTES, [song_id])
    for row in self._cursor.fetchall():
      attributes[row[0]] = row[1]
    return attributes

  def update_song_attributes(self, song_id, attributes):
    SQL_UPSERT_ATTRIBUTE = """
      INSERT INTO attributes
      (song_id, name, value) VALUES (%s, %s, %s)
      ON CONFLICT (song_id, name) DO
      UPDATE SET value = EXCLUDED.value;
    """
    for key, value in attributes.items():
      self._cursor.execute(SQL_UPSERT_ATTRIBUTE, [song_id, key, value])

  def get_tags(self, song_id):
    SQL_SELECT_TAGS = """
      SELECT tags.user_id, tagdefs.name, tags.value
      FROM tags as tags
      JOIN tag_definitions as tagdefs ON tags.tag_id = tagdefs.id;
    """
    tags = {}
    self._cursor.execute(SQL_SELECT_TAGS, [song_id])
    for row in self._cursor.fetchall():
      user_id = row[0]
      tag = row[1]
      value = row[2]
      if tag in tags:
        users = tags[tag]
      else:
        users = {}
        tags[tag] = users
      users[user_id] = value
    return tags
