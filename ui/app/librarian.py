import taglib


READONLY_TAGS = {'bitrate', 'length', 'samplerate', 'sampleRate'}


def read_song_attributes(mp3_filename):
  song = taglib.File(mp3_filename)
  tags = {k.lower(): v[0] for k, v in song.tags.items()}
  tags['bitrate'] = str(song.bitrate)
  tags['length'] = str(song.length)
  tags['samplerate'] = str(song.sampleRate)
  return tags


def write_song_attributes(mp3_filename, attributes):
  pass
