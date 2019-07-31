import logging
import sys

from app import player, resources, sessions, uploads
from app.lib.flaskapp import app
from app.lib import dbinit

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
log = logging.getLogger('streamtagger')

def main(argv):
  del argv

  dbinit.init_db()

  log.info('Starting webserver...')
  app.run(host='localhost', port=5000)

if __name__ == '__main__':
  main(sys.argv)
