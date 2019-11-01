import datetime
import threading


class Job(object):
  def __init__(self):
    self._lock = threading.RLock()
    self._messages = []
    self._active = False

  def start(self, method):
    def task():
      self._active = True
      self.log('Started')
      method(self)
      self.log('Finished')
      self._active = False
    threading.Thread(target=task, daemon=True).start()

  def is_active(self):
    return self._active

  def log(self, message):
    with self._lock:
      self._messages.append((datetime.datetime.utcnow(), message))

  def get_logs(self):
    with self._lock:
      return [msg for msg in self._messages]
