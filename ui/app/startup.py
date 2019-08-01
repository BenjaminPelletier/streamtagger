import logging

from .lib import dbinit

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
log = logging.getLogger('streamtagger')

log.info('Initializing database...')
dbinit.init_db()
