import datetime
import hashlib
import os
import threading
import uuid


from app import dbx
from app.models import Session, Song, Tag, TagDefinition, User
from . import tags
from .song import SongSummary


# https://www.iconfinder.com/iconsets/media-cartoony

PASSWORD_SALT = 'K80Tgi^w1&jc'

#TODO: this is probably not necessary given the nature of SQLAlchemy's session?
_transaction_lock = threading.Lock()


def transaction():
  return Transaction()


class Transaction(object):
  def __init__(self):
    self._committed = False

  def __enter__(self):
    _transaction_lock.acquire()
    return self

  def commit(self):
    dbx.session.commit()
    self._committed = True

  def __exit__(self, type, value, traceback):
    if not self._committed:
      dbx.session.rollback()
    dbx.session.close() #TODO: does Flask-SQLAlchemy manage this automatically?
    _transaction_lock.release()

  def init_database(self):
    dbx.create_all()

  def add_user(self, username, password):
    salted_password = (
        PASSWORD_SALT + username + password + PASSWORD_SALT + username).encode('ascii', 'backslashreplace')
    password_hash = hashlib.sha1(salted_password).hexdigest()
    return self.add_user_with_hash(username, password_hash)

  def add_user_with_hash(self, username, password_hash):
    user = User(username=username, password_hash=password_hash)
    dbx.session.add(user)
    dbx.session.flush()
    return user.id

  def update_user_with_hash(self, username, password_hash):
    user = User.query.filter(User.username == username).one()
    user.password_hash = password_hash
    dbx.session.flush()

  def get_user(self, username):
    user = User.query.filter(User.username == username).one_or_none()
    if user:
      return user.id, user.password_hash
    else:
      return None, None

  def get_users(self):
    users = User.query.all()
    return {user.id: user.username for user in users}

  def add_session(self, user_id, ip):
    now = datetime.datetime.utcnow()
    user_session = Session(user_id=user_id, created_at=now, created_ip=ip, last_used=now)
    dbx.session.add(user_session)
    dbx.session.flush()
    return str(user_session.id)

  def get_session(self, session_id):
    session = Session.query.get(session_id)
    if session:
      return session.user_id, session.last_used
    else:
      return None, None

  def add_song(self, path, title, artist, user_id, username, added_at=None, song_id=None):
    if not added_at:
      added_at = datetime.datetime.utcnow()
    timestamp = added_at.isoformat()
    song = Song(
      path=path,
      title=title,
      artist=artist,
      added_at=added_at,
      added_by=user_id)
    if song_id:
      song.id = song_id
    dbx.session.add(song)
    dbx.session.flush()
    song_id = song.id
    return SongSummary(song_id=song_id, path=path, title=title, artist=artist, added_at=timestamp, added_by=username)

  def update_song(self, summary):
    SQL_UPDATE_SONG = """
      UPDATE songs
      SET (path, title, artist, added_at, added_by) = (%s, %s, %s, %s, u.id)
      FROM songs s JOIN users u ON u.username = %s
      WHERE songs.id = %s;
    """
    self._transaction.execute(SQL_UPDATE_SONG,
                              [summary.path, summary.title, summary.artist, summary.added_at, summary.added_by,
                          str(summary.song_id)])

  def get_tag_ids(self, tag_names):
    ids = {}
    SQL_FIND_TAGS = """
      SELECT id, name
      FROM tag_definitions
      WHERE name IN %s
    """
    self._transaction.execute(SQL_FIND_TAGS, (tag_names,))
    for row in self._transaction.fetchall():
      ids[row[1]] = row[0]

  def get_tag_definitions(self):
    return {tagdef.name: tags.TagDefinition(
              id=tagdef.id,
              name=tagdef.name,
              type=tagdef.type,
              created_by=tagdef.created_by,
              created_at=tagdef.created_at)
            for tagdef in TagDefinition.query.all()}

  def get_tag_types(self):
    return {tag_def.name: tag_def.type for tag_def in self.get_tag_definitions().values()}

  def create_tag_definition(self, name, tag_type, user_id):
    SQL_CREATE_TAG_DEFINITION = """
      INSERT INTO tag_definitions
      (name, type, created_by, created_at) VALUES (%s, %s, %s, %s)
      RETURNING id;
    """
    timestamp = datetime.datetime.utcnow().isoformat()
    self._transaction.execute(SQL_CREATE_TAG_DEFINITION, (name, tag_type, user_id, timestamp))
    row = self._transaction.fetchone()
    return row[0]

  def set_label(self, tag_def_id, song_id, user_id, value):
    SQL_UPSERT_TAG = """
      INSERT INTO tags
      (tag_id, song_id, user_id, value, last_changed) VALUES (%s, %s, %s, %s, %s)
      ON CONFLICT (tag_id, song_id, user_id) DO
      UPDATE SET (value, last_changed) = (EXCLUDED.value, EXCLUDED.last_changed);
    """
    timestamp = datetime.datetime.utcnow().isoformat()
    self._transaction.execute(SQL_UPSERT_TAG, [str(tag_def_id), str(song_id), str(user_id), value, timestamp])

  def clear_label(self, tag_def_id, song_id, user_id):
    SQL_REMOVE_TAG = """
      DELETE FROM tags
      WHERE tag_id = %s AND song_id = %s AND user_id = %s;
    """
    self._transaction.execute(SQL_REMOVE_TAG, [str(tag_def_id), str(song_id), str(user_id)])

  def get_tags(self, song_ids):
    song_tags = Tag.query.filter(Tag.song_id.in_(song_ids)).all()
    tags_by_song = {}
    tag_names = set()
    tagdefs = self.get_tag_definitions()
    for tag in song_tags:
      song_id = uuid.UUID(str(tag.song_id))
      if song_id in tags_by_song:
        tagset = tags_by_song[song_id]
      else:
        tagset = tags.TagSet()
        tags_by_song[song_id] = tagset
      tagset.add_label(tag.tag.name, tagdefs[tag.tag.name], tag.user.username, tag.value, tag.last_changed)
      tag_names.add(tag.tag.name)
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
    song = Song.query.filter(Song.path.like(path)).first()
    return song.song_id if song else None

  def delete_song(self, song_id):
    SQL_DELETE_SONG = """
      DELETE FROM songs WHERE id = %s;
    """ % str(song_id)
    dbx.engine.execute(SQL_DELETE_SONG)

  def get_songs_by_ids(self, song_ids):
    Song.query.filter(Song.id.in_(song_ids)).all()
    return [SongSummary(
              song_id=song.id,
              title=song.title,
              artist=song.artist,
              path=song.path,
              added_at=song.added_at,
              added_by=song.user.username if song.user else None)
            for song in map(Song.query.get, song_ids)]

  def get_song_by_id(self, song_id):
    return self.get_songs_by_ids([song_id])[0]

  def query_songs(self, where_clauses):
    if where_clauses:
      song_ids = None
      for where_clause in where_clauses:
        SQL_SELECT_SONG_IDS = """
          SELECT songs.id
          FROM songs as songs
          JOIN tags ON tags.song_id = songs.id
          WHERE %s
          ORDER BY songs.added_at DESC
        """ % where_clause
        result = dbx.engine.execute(SQL_SELECT_SONG_IDS)
        new_ids = set(row[0] for row in result)
        if song_ids:
          song_ids = song_ids.intersection(new_ids)
        else:
          song_ids = set(new_ids)
    else:
      songs = Song.query.order_by(Song.added_at.desc()).all()
      song_ids = [song.id for song in songs]
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
    self._transaction.execute(SQL_FIND_SONGS_BY_ARTIST)
    songs_with_artist = {row[0] for row in self._transaction.fetchall()}
    self._transaction.execute(SQL_FIND_SONGS_BY_TITLE)
    songs_with_title = {row[0] for row in self._transaction.fetchall()}
    song_ids = songs_with_artist.intersection(songs_with_title)
    return self.get_songs_by_ids(song_ids)
