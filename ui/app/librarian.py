from mutagen.id3 import ID3
from mutagen.easyid3 import EasyID3
import taglib


READONLY_TAGS = {'bitrate', 'length', 'samplerate', 'sampleRate'}


def read_song_attributes(mp3_filename):
  # id3 = ID3(mp3_filename)
  song = taglib.File(mp3_filename)
  tags = {k.lower(): v[0] for k, v in song.tags.items()}
  tags['bitrate'] = str(song.bitrate)
  tags['length'] = str(song.length)
  tags['samplerate'] = str(song.sampleRate)
  return tags


class AttributesWriteError(RuntimeError):
  def __init__(self, message):
    RuntimeError.__init__(self, message)


def write_song_attributes(mp3_filename, attributes):
  song = taglib.File(mp3_filename)
  for k, v in attributes.items():
    if k not in READONLY_TAGS:
      song.tags[k] = v
  try:
    unsaved_tags = None # song.save()
  except OSError as e:
    raise AttributesWriteError('OSError: ' + str(e))
  except ValueError as e:
    raise AttributesWriteError('ValueError: ' + str(e))
  if unsaved_tags:
    raise AttributesWriteError('Unable to save tags {%s}' % ', '.join(unsaved_tags))

