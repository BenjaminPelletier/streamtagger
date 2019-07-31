import logging
import sys

from app.lib import db

def main(argv):
  del argv
  # Ensure database is blank
  with db.transaction() as transaction:
    transaction.clear_database()
    transaction.commit()

  # Initialize blank database
  with db.transaction() as transaction:
    transaction.init_database()
    transaction.commit()

  # Add user
  with db.transaction() as transaction:
    user_id = transaction.add_user('user1', 'password')
    transaction.commit()

  # Add session for user
  with db.transaction() as transaction:
    session_id = transaction.add_session(user_id, 'localhost')
    transaction.commit()

  # Add song without any tags
  with db.transaction() as transaction:
    song_id_1 = transaction.add_song('201907/x.mp3', session_id)
    transaction.commit()

  # Add song with tags
  with db.transaction() as transaction:
    song_id_2 = transaction.add_song('201907/y.mp3', session_id)
    tags = ('tag1', 'tag2')
    tagdef_ids = transaction.get_tag_ids(tags, user_id)
    for tagdef_id in tagdef_ids.values():
      transaction.set_tag(tagdef_id, song_id_2, user_id, 1)
    transaction.commit()

  # Add song with overlapping tags
  with db.transaction() as transaction:
    song_id_3 = transaction.add_song('201907/z.mp3', session_id)
    tags = ('tag2', 'tag3')
    tagdef_ids = transaction.get_tag_ids(tags, user_id)
    for tagdef_id in tagdef_ids.values():
      transaction.set_tag(tagdef_id, song_id_3, user_id, 1)
    transaction.commit()

  # Add tag
  with db.transaction() as transaction:
    tagdef_id = transaction.get_tag_id('tag1', user_id)
    transaction.set_tag(tagdef_id, song_id_1, user_id, 1)
    transaction.commit()

  # Modify tag
  with db.transaction() as transaction:
    tagdef_id = transaction.get_tag_id('tag1', user_id)
    transaction.set_tag(tagdef_id, song_id_2, user_id, -1)
    transaction.commit()

  # Remove tag
  with db.transaction() as transaction:
    tagdef_id = transaction.get_tag_id('tag2', user_id)
    transaction.clear_tag(tagdef_id, song_id_2, user_id)
    transaction.commit()

  # Query songs
  with db.transaction() as transaction:
    songs = transaction.query_songs('')
  for song in songs:
    print('%s: %s at %s by %s | %s | %s' % (song.song_id, song.path, song.added, song.added_by, song.attributes, song.tags))


if __name__ == '__main__':
  main(sys.argv)
