import collections
import datetime
import json


TagDefinition = collections.namedtuple('TagDefinition', ('id', 'name', 'type', 'created_by', 'created_at'))


class TagSet(dict):
  def __init__(self, json_str=None, tag_types=None):
    super(TagSet, self).__init__()

    if json_str:
      if tag_types is None:
        tag_types = {}
      tag_dict = json.loads(json_str)
      for name, tag in tag_dict.items():
        self[name] = Tag.from_json_dict(name, tag_types.get(name), tag)

  def get_user_label_entries(self, username):
    tag_values = {}
    for tag_name, tag in self.items():
      if username in tag:
        value = tag[username].value
        if tag.tag_type in {Tag.TYPE_THUMBS_UP_DOWN, Tag.TYPE_STARS, Tag.TYPE_FACES}:
          tag_values[tag_name] = tag_name + ':%d' % value
        else:  # Assume TYPE_HASH
          tag_values[tag_name] = tag_name
    return tag_values

  def to_json(self):
    return json.dumps({tag.name: tag.to_json_dict() for tag in self})


class Tag(dict):
  TYPE_HASH = 'hashtag'
  TYPE_THUMBS_UP_DOWN = 'thumbsupdown'
  TYPE_STARS = 'stars'
  TYPE_FACES = 'faces'
  TYPES = {TYPE_HASH, TYPE_THUMBS_UP_DOWN, TYPE_STARS, TYPE_FACES}

  def __init__(self, name, tag_type):
    super(Tag, self).__init__()
    self.name = name
    self.tag_type = tag_type

  def add_label(self, username, value, last_changed):
    self[username] = Label(username, value, last_changed)

  def to_json_dict(self):
    return {label.username: label.to_json_dict() for label in self.values()}

  @staticmethod
  def from_json_dict(name, tag_type, tag):
    result = Tag(name, tag_type)
    for username, label_dict in tag.items():
      result[username] = Label.from_json_dict(username, label_dict)


class Label(object):
  def __init__(self, username, value, last_changed):
    assert isinstance(value, int)
    assert isinstance(last_changed, datetime.datetime)
    self.username = username
    self.value = value
    self.last_changed = last_changed

  def to_json_dict(self):
    return {'v': self.value, 't': self.last_changed.isoformat()}

  @staticmethod
  def from_json_dict(username, label):
    last_changed = datetime.datetime.strptime(label['t'], '%Y-%m-%dT%H:%M:%S.%f')
    return Label(username, label['v'], last_changed)
