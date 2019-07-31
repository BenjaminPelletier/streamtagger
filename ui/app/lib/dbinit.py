import random

from . import db

def init_db():
  with db.transaction() as transaction:
    transaction.init_database()
    users = transaction.get_users()
    if not users:
      r = random.Random()
      password =  ''.join(r.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for i in range(10))
      transaction.add_user('admin', password)
    else:
      password = None
    transaction.commit()
  if password:
    print('Password for admin is ' + password)
