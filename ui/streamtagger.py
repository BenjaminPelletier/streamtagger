import logging
import sys

from app import player, song_details, song_by_artist_title, resources, sessions, uploads, users, song_list, sync, tags, startup
from app.lib.flaskapp import app
from app.lib import dbinit

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
log = logging.getLogger('streamtagger')

def main(argv):
  del argv

  log.info('Starting webserver...')
  app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
  main(sys.argv)
