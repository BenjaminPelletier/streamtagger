import datetime
import hashlib
import os
import threading
import uuid

from . import tags
from .song import SongSummary

import psycopg2

# https://www.iconfinder.com/iconsets/media-cartoony

PASSWORD_SALT = 'K80Tgi^w1&jc'

_connection = None
_transaction_lock = None

def reconnect():
  global _connection, _transaction_lock
  _connection = psycopg2.connect(os.environ.get('ST_DB_CONNECTIONSTRING'))
  _transaction_lock = threading.Lock()

reconnect()

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
        title VARCHAR NOT NULL,
        artist VARCHAR,
        added_at TIMESTAMP NOT NULL,
        added_by UUID REFERENCES users (id) ON DELETE RESTRICT
      );
    """

    SQL_CREATE_TAG_DEFINITIONS_TABLE = """
      CREATE TABLE IF NOT EXISTS tag_definitions (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        name VARCHAR NOT NULL UNIQUE,
        type VARCHAR NOT NULL,
        created_by UUID REFERENCES users (id) ON DELETE RESTRICT,
        created_at TIMESTAMP NOT NULL
      );
    """

    SQL_CREATE_TAGS_TABLE = """
      CREATE TABLE IF NOT EXISTS tags (
        tag_id UUID NOT NULL REFERENCES tag_definitions (id) ON DELETE CASCADE,
        song_id UUID NOT NULL REFERENCES songs (id) ON DELETE CASCADE,
        user_id UUID NOT NULL REFERENCES users (id) ON DELETE CASCADE,
        value INT,
        last_changed TIMESTAMP NOT NULL,
        PRIMARY KEY (tag_id, song_id, user_id)
      );
    """

    self._cursor.execute(SQL_ENABLE_CRYPTO)
    self._cursor.execute(SQL_CREATE_USERS_TABLE)
    self._cursor.execute(SQL_CREATE_SESSIONS_TABLE)
    self._cursor.execute(SQL_CREATE_SONGS_TABLE)
    self._cursor.execute(SQL_CREATE_TAG_DEFINITIONS_TABLE)
    self._cursor.execute(SQL_CREATE_TAGS_TABLE)

  def add_user(self, username, password):
    salted_password = (PASSWORD_SALT + password + PASSWORD_SALT).encode('ascii', 'backslashreplace')
    password_hash = hashlib.sha1(salted_password).hexdigest()
    return self.add_user_with_hash(username, password_hash)

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

  def add_song(self, path, title, artist, user_id, username, added_at=None, song_id=None):
    if not added_at:
      added_at = datetime.datetime.utcnow()
    timestamp = added_at.isoformat()
    if not song_id:
      SQL_INSERT_SONG = """
        INSERT INTO songs
        (path, title, artist, added_at, added_by) VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
      """
      self._cursor.execute(SQL_INSERT_SONG, [path, title, artist, timestamp, user_id])
    else:
      SQL_INSERT_SONG = """
        INSERT INTO songs
        (id, path, title, artist, added_at, added_by) VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id;
      """
      self._cursor.execute(SQL_INSERT_SONG, [str(song_id), path, title, artist, timestamp, user_id])
    row = self._cursor.fetchone()
    song_id = row[0]
    return SongSummary(song_id=song_id, path=path, title=title, artist=artist, added_at=timestamp, added_by=username)

  def update_song(self, summary):
    SQL_UPDATE_SONG = """
      UPDATE songs
      SET (path, title, artist, added_at, added_by) = (%s, %s, %s, %s, u.id)
      FROM songs s JOIN users u ON u.username = %s
      WHERE songs.id = %s;
    """
    self._cursor.execute(SQL_UPDATE_SONG,
                         [summary.path, summary.title, summary.artist, summary.added_at, summary.added_by,
                          str(summary.song_id)])

  def get_tag_ids(self, tag_names):
    ids = {}
    SQL_FIND_TAGS = """
      SELECT id, name
      FROM tag_definitions
      WHERE name IN %s
    """
    self._cursor.execute(SQL_FIND_TAGS, (tag_names,))
    for row in self._cursor.fetchall():
      ids[row[1]] = row[0]

  def get_tag_definitions(self):
    SQL_GET_TAG_DEFINITIONS = """
      SELECT id, name, type, created_by, created_at
      FROM tag_definitions
    """
    tag_defs = {}
    self._cursor.execute(SQL_GET_TAG_DEFINITIONS)
    for row in self._cursor.fetchall():
      tag_defs[row[1]] = tags.TagDefinition(id=row[0], name=row[1], type=row[2], created_by=row[3], created_at=row[4])
    return tag_defs

  def get_tag_types(self):
    return {tag_def.name: tag_def.type for tag_def in self.get_tag_definitions().values()}

  def create_tag_definition(self, name, tag_type, user_id):
    SQL_CREATE_TAG_DEFINITION = """
      INSERT INTO tag_definitions
      (name, type, created_by, created_at) VALUES (%s, %s, %s, %s)
      RETURNING id;
    """
    timestamp = datetime.datetime.utcnow().isoformat()
    self._cursor.execute(SQL_CREATE_TAG_DEFINITION, (name, tag_type, user_id, timestamp))
    row = self._cursor.fetchone()
    return row[0]

  def set_label(self, tag_def_id, song_id, user_id, value):
    SQL_UPSERT_TAG = """
      INSERT INTO tags
      (tag_id, song_id, user_id, value, last_changed) VALUES (%s, %s, %s, %s, %s)
      ON CONFLICT (tag_id, song_id, user_id) DO
      UPDATE SET (value, last_changed) = (EXCLUDED.value, EXCLUDED.last_changed);
    """
    timestamp = datetime.datetime.utcnow().isoformat()
    self._cursor.execute(SQL_UPSERT_TAG, [str(tag_def_id), str(song_id), str(user_id), value, timestamp])

  def clear_label(self, tag_def_id, song_id, user_id):
    SQL_REMOVE_TAG = """
      DELETE FROM tags
      WHERE tag_id = %s AND song_id = %s AND user_id = %s;
    """
    self._cursor.execute(SQL_REMOVE_TAG, [tag_def_id, song_id, user_id])

  def get_tags(self, song_ids):
    users = self.get_users()
    SQL_SELECT_TAGS = """
      SELECT tags.song_id, tags.user_id, tagdefs.type, tags.last_changed, tagdefs.name, tags.value
      FROM tags as tags
      JOIN tag_definitions as tagdefs ON tags.tag_id = tagdefs.id
      WHERE tags.song_id in (%s)
    """
    tagdefs = self.get_tag_definitions()
    tag_names = set()
    song_id_list = ', '.join("'%s'" % id for id in song_ids)
    query = SQL_SELECT_TAGS % song_id_list
    self._cursor.execute(query)
    tags_by_song = {}
    for row in self._cursor.fetchall():
      song_id, user_id, tag_type, last_changed, tag_name, tag_value = row
      song_id = uuid.UUID(song_id)
      username = users[user_id]
      if song_id in tags_by_song:
        tagset = tags_by_song[song_id]
      else:
        tagset = tags.TagSet()
        tags_by_song[song_id] = tagset
      tagset.add_label(tag_name, tagdefs[tag_name], username, tag_value, last_changed)
      tag_names.add(tag_name)
    return tags_by_song, tag_names

  def get_tags_for_song(self, song_id):
    if not isinstance(song_id, uuid.UUID):
      song_id = uuid.UUID(song_id)
    tags_by_song, tag_names = self.get_tags([song_id])
    return tags_by_song.get(song_id, tags.TagSet())

  def synchronize_tags(self, song_id, tagset):
    tagsets_by_song, tag_names = self.get_tags([song_id])
    db_tagset = tagsets_by_song[uuid.UUID(song_id)]
    user_ids = {v: k for k, v in self.get_users().items()}
    tagdef_ids = {tagdef.name: tagdef.id for tagdef in self.get_tag_definitions().values()}

    # Add tags from tagset that aren't in db_tagset
    for tag in tagset.values():
      tagdef_id = tagdef_ids[tag.name]
      db_tag = db_tagset.get(tag.name, tags.Tag(tag.name))
      for label in tag.values():
        if label.username not in db_tag or label.value != db_tag[label.username].value:
          self.set_label(tagdef_id, song_id, user_ids[label.username], label.value)

    # Remove tags from db_tagset that aren't in tagset
    for db_tag in db_tagset.values():
      tagdef_id = tagdef_ids[db_tag.name]
      tag = tagset.get(db_tag.name, tags.Tag(db_tag.name))
      for db_label in db_tag.values():
        if db_label.username not in tag:
          self.clear_label(tagdef_id, song_id, user_ids[db_label.username])

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

  def get_songs_by_ids(self, song_ids):
    SQL_SELECT_SONGS = """
      SELECT
        songs.id, songs.title, songs.artist, songs.path, songs.added_at, songs.added_by
      FROM songs as songs
      WHERE songs.id IN (%s)
      ORDER BY songs.added_at DESC;
    """
    if not song_ids:
      return []
    song_id_list = ', '.join("'%s'" % id for id in song_ids)
    query = SQL_SELECT_SONGS % song_id_list
    songs = []
    users = None
    self._cursor.execute(query)
    for row in self._cursor.fetchall():
      if users is None:
        users = self.get_users()
      songs.append(SongSummary(
        song_id=row[0], title=row[1], artist=row[2], path=row[3], added_at=row[4], added_by=users.get(row[5])))
    return songs

  def query_songs(self, where_clause):
    SQL_SELECT_SONG_IDS = """
      SELECT songs.id
      FROM songs as songs
      ORDER BY songs.added_at DESC
    """
    if where_clause:
      SQL_SELECT_SONG_IDS += ' WHERE ' + where_clause
    self._cursor.execute(SQL_SELECT_SONG_IDS)
    song_ids = [row[0] for row in self._cursor.fetchall()]
    return self.get_songs_by_ids(song_ids)

  def find_songs_by_artist_title(self, artist, title):
    SQL_FIND_SONGS_BY_ARTIST = """
      SELECT id
      FROM songs
      WHERE artist ILIKE '%%%s%%';
    """ % artist
    SQL_FIND_SONGS_BY_TITLE = """
      SELECT id
      FROM songs
      WHERE title ILIKE '%%%s%%';
    """ % title
    self._cursor.execute(SQL_FIND_SONGS_BY_ARTIST)
    songs_with_artist = {row[0] for row in self._cursor.fetchall()}
    self._cursor.execute(SQL_FIND_SONGS_BY_TITLE)
    songs_with_title = {row[0] for row in self._cursor.fetchall()}
    song_ids = songs_with_artist.intersection(songs_with_title)
    return self.get_songs_by_ids(song_ids)
