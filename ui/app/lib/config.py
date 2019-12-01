import os

class Config(object):
  # media_path should not have a trailing /
  media_path = os.environ.get('ST_MEDIA_PATH', '/var/media')
