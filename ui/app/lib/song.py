import os


class Song(object):
  TITLE_KEY = 'title'
  ARTIST_KEYS = ('artist', 'albumartist')

  def __init__(self, song_id, path, added, added_by, attributes, tags):
    self.song_id = song_id
    self.path = path
    self.added = added
    self.added_by = added_by
    self.attributes = attributes
    self.tags = tags

  def get_title(self):
    if Song.TITLE_KEY in self.attributes:
      return self.attributes[Song.TITLE_KEY]
    parts = os.path.split(self.path)
    return os.path.splitext(parts[-1])[0]

  def get_title_key(self):
    return Song.TITLE_KEY

  def get_artist(self):
    key = self.get_artist_key()
    return self.attributes[key] if key else ''

  def get_artist_key(self):
    for key in Song.ARTIST_KEYS:
      if key in self.attributes:
        return key
    return None

  def set_title(self, title):
    self.attributes[Song.TITLE_KEY] = title

  def set_artist(self, artist):
    key = self.get_artist_key()
    if key is None:
      key = Song.ARTIST_KEYS[0]
    self.attributes[key] = artist

  def get_added_at(self):
    return self.added.isoformat()
