import datetime
import os
import uuid

from . import tags

import mutagen.id3


class SongSummary(object):
  """Representation of a song in the database for quick lookup"""

  def __init__(self, song_id, title, artist, path, added_at, added_by):
    self.song_id = uuid.UUID(song_id)
    self.title = title
    self.artist = artist
    self.path = path
    self.added_at = added_at
    self.added_by = added_by


class SongDetails(object):
  """Full representation of song; ground truth from MP3 file's ID3 tags"""

  TXXX_PREFIX = 'TXXX:'
  DESC_PREFIX = 'StreamTagger: '
  DESC_ADDED_BY = DESC_PREFIX + 'AddedBy'
  DESC_ADDED_AT = DESC_PREFIX + 'AddedAt'
  DESC_SONG_ID = DESC_PREFIX + 'SongId'
  DESC_TAGS = DESC_PREFIX + 'Tags'

  def __init__(self, mp3_filename):
    self._filename = mp3_filename
    try:
      self._id3 = mutagen.id3.ID3(mp3_filename)
    except mutagen.id3.ID3NoHeaderError:
      self._id3 = mutagen.id3.ID3()

  def make_summary(self, media_path, summary=None):
    to_update = []
    if summary:
      if summary.title != self.title:
        to_update.append(('title', summary.title, self.title))
      if summary.artist != self.artist:
        to_update.append(('artist', summary.artist, self.artist))
      if summary.added_at != self.added_at:
        to_update.append(('added_at', summary.added_at, self.added_at))
      if summary.added_by != self.added_by:
        to_update.append(('added_by', summary.added_by, self.added_by))
      if summary.path != media_path:
        to_update.append(('path', summary.path, media_path))
    return SongSummary(
      song_id=str(summary.song_id if summary else self.song_id),
      title=self.title,
      artist=self.artist,
      added_at=self.added_at,
      added_by=self.added_by,
      path=media_path), to_update

  def save(self):
    self._id3.save(filename=self._filename, v2_version=3)

  def get_title(self):
    frame = self._id3.get('TIT2')
    if frame:
      return frame.text[0]
    parts = os.path.split(self._filename)
    return os.path.splitext(parts[-1])[0]

  def set_title(self, title):
    frame = mutagen.id3.TIT2(text=title)
    self._id3.add(frame)

  title = property(get_title, set_title)


  def get_artist(self):
    frame = self._id3.get('TOPE')
    if frame:
      return frame.text[0]
    frame = self._id3.get('TPE1')
    if frame:
      return frame.text[0]
    frame = self._id3.get('TPE2')
    if frame:
      return frame.text[0]
    return None

  def set_artist(self, artist):
    frame = mutagen.id3.TOPE(text=artist)
    self._id3.add(frame)

  artist = property(get_artist, set_artist)


  def get_added_by(self):
    frame = self._id3.get(SongDetails.TXXX_PREFIX + SongDetails.DESC_ADDED_BY)
    return None if frame is None else frame.text[0]

  def set_added_by(self, username):
    if username is None:
      self._id3.pop(SongDetails.TXXX_PREFIX + SongDetails.DESC_ADDED_BY, None)
    else:
      frame = mutagen.id3.TXXX(desc=SongDetails.DESC_ADDED_BY, text=[username])
      self._id3.add(frame)

  added_by = property(get_added_by, set_added_by)


  def get_added_at(self):
    frame = self._id3.get(SongDetails.TXXX_PREFIX + SongDetails.DESC_ADDED_AT)
    if frame is None:
      return None
    try:
      # return datetime.datetime.fromisoformat(frame.text[0]) (Python 3.7+)
      return datetime.datetime.strptime(frame.text[0], '%Y-%m-%dT%H:%M:%S.%f')
    except ValueError:
      # TODO: log warning
      return None

  def set_added_at(self, timestamp):
    if timestamp is None:
      self._id3.pop(SongDetails.TXXX_PREFIX + SongDetails.DESC_ADDED_AT, None)
    else:
      frame = mutagen.id3.TXXX(desc=SongDetails.DESC_ADDED_AT, text=[timestamp.isoformat()])
      self._id3.add(frame)

  added_at = property(get_added_at, set_added_at)


  def get_song_id(self):
    frame = self._id3.get(SongDetails.TXXX_PREFIX + SongDetails.DESC_SONG_ID)
    if frame is None:
      return None
    try:
      return uuid.UUID(frame.text[0])
    except ValueError:
      # TODO: log warning
      return None

  def set_song_id(self, song_id):
    if song_id is None:
      self._id3.pop(SongDetails.TXXX_PREFIX + SongDetails.DESC_SONG_ID, None)
    else:
      frame = mutagen.id3.TXXX(desc=SongDetails.DESC_SONG_ID, text=[str(song_id)])
      self._id3.add(frame)

  song_id = property(get_song_id, set_song_id)


  def get_tags(self):
    """Retrieve all tags associated with this song.

    :return: dict relating tag name to tags.Tag.
    """
    frame = self._id3.get(SongDetails.TXXX_PREFIX + SongDetails.DESC_TAGS)
    if frame is None:
      return tags.TagSet()
    try:
      return tags.TagSet(json_str=frame.text[0], tag_types={}) #TODO: include tag types
    except ValueError:
      # TODO: log warning
      return tags.TagSet()

  def set_tags(self, new_tags):
    assert isinstance(new_tags, tags.TagSet)
    if new_tags:
      frame = mutagen.id3.TXXX(desc=SongDetails.DESC_TAGS, text=[new_tags.to_json()])
      self._id3.add(frame)
    else:
      self._id3.pop(SongDetails.TXXX_PREFIX + SongDetails.DESC_TAGS, None)

  tags = property(get_tags, set_tags)
