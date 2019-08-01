import datetime
import os


class Song(object):
  def __init__(self, song_id, path, added, added_by, attributes, tags):
    self.song_id = song_id
    self.path = path
    self.added = added
    self.added_by = added_by
    self.attributes = attributes
    self.tags = tags

  def get_title(self):
    if 'title' in self.attributes:
      return self.attributes['title']
    parts = os.path.split(self.path)
    return os.path.splitext(parts[-1])[0]

  def get_artist(self):
    if 'artist' in self.attributes:
      return self.attributes['artist']
    return ''

  def get_added_at(self):
    return self.added.isoformat()
