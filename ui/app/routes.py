from app import app

@app.route('/status')
def status():
  return 'Ok'

from . import player, resources, sessions, song_by_artist_title, song_details, song_list, sync, tags, uploads, users, playlists

from . import startup
