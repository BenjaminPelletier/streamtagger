from app import dbx
from .lib.db_uuid import UUID

from sqlalchemy.orm import relationship


class User(dbx.Model):
    __tablename__ = 'users'

    id = dbx.Column(UUID, primary_key=True, server_default=dbx.text("gen_random_uuid()"))
    username = dbx.Column(dbx.String, unique=True)
    password_hash = dbx.Column(dbx.String, nullable=False)

    def __repr__(self):
      return '<User {}>'.format(self.username)


class Session(dbx.Model):
    __tablename__ = 'sessions'

    id = dbx.Column(UUID, primary_key=True, server_default=dbx.text("gen_random_uuid()"))
    user_id = dbx.Column(dbx.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created_at = dbx.Column(dbx.DateTime, nullable=False)
    created_ip = dbx.Column(dbx.String, nullable=False)
    last_used = dbx.Column(dbx.DateTime, nullable=False)

    user = relationship('User')

    def __repr__(self):
      return '<Session {} by {}>'.format(self.id, self.user)


class Song(dbx.Model):
    __tablename__ = 'songs'

    id = dbx.Column(UUID, primary_key=True, server_default=dbx.text("gen_random_uuid()"))
    path = dbx.Column(dbx.String, nullable=False, unique=True)
    title = dbx.Column(dbx.String, nullable=False)
    artist = dbx.Column(dbx.String)
    added_at = dbx.Column(dbx.DateTime, nullable=False)
    added_by = dbx.Column(dbx.ForeignKey('users.id', ondelete='RESTRICT'))

    user = relationship('User')

    def __repr__(self):
      return '<Song {}>'.format(self.title)


class TagDefinition(dbx.Model):
    __tablename__ = 'tag_definitions'

    id = dbx.Column(UUID, primary_key=True, server_default=dbx.text("gen_random_uuid()"))
    name = dbx.Column(dbx.String, nullable=False, unique=True)
    type = dbx.Column(dbx.String, nullable=False)
    created_by = dbx.Column(dbx.ForeignKey('users.id', ondelete='RESTRICT'))
    created_at = dbx.Column(dbx.DateTime, nullable=False)

    user = relationship('User')

    def __repr__(self):
      return '<TagDef {}>'.format(self.name)


class Tag(dbx.Model):
    __tablename__ = 'tags'

    tag_id = dbx.Column(dbx.ForeignKey('tag_definitions.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    song_id = dbx.Column(dbx.ForeignKey('songs.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    user_id = dbx.Column(dbx.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    value = dbx.Column(dbx.Integer)
    last_changed = dbx.Column(dbx.DateTime, nullable=False)

    song = relationship('Song')
    tag = relationship('TagDefinition')
    user = relationship('User')

    def __repr__(self):
      return '<Tag {} on {} by {}>'.format(self.tag.name, self.song.title, self.user.name)
