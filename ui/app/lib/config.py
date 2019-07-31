import os

media_path = os.environ.get('ST_MEDIA_PATH', '/var/media')
if media_path[-1] != '/':
  media_path += '/'
