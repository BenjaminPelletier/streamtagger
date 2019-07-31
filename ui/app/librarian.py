import taglib

def read_song_attributes(mp3_filename):
  song = taglib.File(mp3_filename)
  print(song.tags)
  return {}
