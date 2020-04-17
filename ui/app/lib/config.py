import os

class Config(object):
  # media_path should not have a trailing /
  media_path = os.environ.get('ST_MEDIA_PATH', '/var/media')

  SQLALCHEMY_DATABASE_URI = os.environ.get('ST_DB_CONNECTIONSTRING')
  SQLALCHEMY_TRACK_MODIFICATIONS = False

  SECRET_KEY = os.environ.get('ST_SECRET_KEY', '').encode('utf-8')

if not Config.SECRET_KEY:
  raise ValueError('The ST_SECRET_KEY environment variable must be set')
