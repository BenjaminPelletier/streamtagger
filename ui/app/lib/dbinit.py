import random

from . import db

def init_db():
  with db.transaction() as transaction:
    users = transaction.get_users()
    if not users:
      raise NotImplementedError("Auto database initialization functionality has not yet been restored")
      transaction.init_database()
      r = random.Random()
      password =  ''.join(r.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for i in range(10))
      with open('admin.password', 'w') as f:
        f.write(password)
      transaction.add_user('admin', password)
      transaction.commit()
    else:
      password = None
  if password:
    print('Password for admin is ' + password)
