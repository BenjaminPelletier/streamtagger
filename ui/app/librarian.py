import taglib

def read_song_attributes(mp3_filename):
  song = taglib.File(mp3_filename)
  tags = {k.lower(): v[0] for k, v in song.tags.items()}
  tags['bitrate'] = str(song.bitrate)
  tags['length'] = str(song.length)
  tags['sampleRate'] = str(song.sampleRate)
  return tags
