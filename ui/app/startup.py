import logging

from .lib.flaskapp import app
from .lib import dbinit

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
log = logging.getLogger('streamtagger')

log.info('Initializing database...')
print('print init db', flush=True)
dbinit.init_db()
