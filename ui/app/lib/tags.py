import collections
import datetime
import json


TagDefinition = collections.namedtuple('TagDefinition', ('type', 'created_at', 'created_by'))


class TagSet(dict):
  def __init__(self, json_str=None):
    super(TagSet, self).__init__()

    if json_str:
      tag_dict = json.loads(json_str)
      for name, tag in tag_dict.items():
        self[name] = Tag.from_json_dict(name, tag)

  def get_user_label_entries(self, username, tag_types):
    label_entries = []
    for tag_name, tag in self.items():
      if username in tag:
        value = tag[username].value
        tag_type = tag_types[tag_name]
        if any(tag_type == t for t in (Tag.TYPE_THUMBS_UP_DOWN, Tag.TYPE_STARS, Tag.TYPE_FACES)):
          label_entries.append(tag_name + ':%d' % value)
        else:  # Assume TYPE_HASH
          label_entries.append(tag_name)
    return label_entries

  def add_label(self, tag_name, tagdef, username, tag_value, last_changed):
    if tag_name in self:
      tag = self[tag_name]
    else:
      tag = Tag(tag_name, tagdef.type)
      self[tag_name] = tag
    tag.add_label(username, tag_value, last_changed)

  def make_report(self, report_name):
    if '@' in report_name:
      username, tag_name = report_name.split('@')
      if tag_name not in self:
        return None
      tag = self[tag_name]
      if username not in tag:
        return None
      return tag[username].value
    else:
      tag_name = report_name
      if tag_name not in self:
        return None
      tag = self[tag_name]
      n = 0
      value = 0
      for label in tag.values():
        value += label.value
        n += 1
      return value / n if n > 0 else None

  def set_user_label_entries(self, entries, username):
    changes = False

    # Add tags/labels for all entries
    entry_tag_names = set()
    for entry in entries:
      if ':' in entry:
        tag_name, value = entry.split(':')
        value = int(value)
      else:
        tag_name = entry
        value = None
      entry_tag_names.add(tag_name)

      if tag_name not in self:
        # The song did not previously contain this tag
        tag = Tag(tag_name)
        tag.add_label(username, value, datetime.datetime.utcnow())
        self[tag_name] = tag
        changes = True
      else:
        tag = self[tag_name]
        if username in tag:
          # The user has an existing label for this tag
          if value != tag[username].value:
            # The user has changed their label
            tag[username].value = value
            changes = True
        else:
          # The user does not have an existing lable for this tag
          tag.add_label(username, value)
          changes = True

    # Check for any tag/label deletions
    tags_to_delete = []
    for tag in self.values():
      if tag.name not in entry_tag_names and username in tag:
        # The user has an existing label for this tag, but didn't include an entry for it; delete the old label
        del tag[username]
        if len(tag) == 0:
          tags_to_delete.append(tag.name)
        changes = True
    for tag_to_delete in tags_to_delete:
      del self[tag_to_delete]

    return changes

  def to_json(self):
    return json.dumps({tag.name: tag.to_json_dict() for tag in self.values()})


class Tag(dict):
  TYPE_HASH = 'hashtag'
  TYPE_THUMBS_UP_DOWN = 'thumbsupdown'
  TYPE_STARS = 'stars'
  TYPE_FACES = 'faces'
  TYPES = {TYPE_HASH, TYPE_THUMBS_UP_DOWN, TYPE_STARS, TYPE_FACES}

  def __init__(self, name):
    super(Tag, self).__init__()
    self.name = name

  def add_label(self, username, value, last_changed=None):
    if not last_changed:
      last_changed = datetime.datetime.utcnow()
    self[username] = Label(username, value, last_changed)

  def to_json_dict(self):
    return {label.username: label.to_json_dict() for label in self.values()}

  @staticmethod
  def from_json_dict(name, tag):
    result = Tag(name)
    for username, label_dict in tag.items():
      result[username] = Label.from_json_dict(username, label_dict)
    return result


class Label(object):
  def __init__(self, username, value, last_changed):
    assert isinstance(last_changed, datetime.datetime)
    self.username = username
    self.value = value
    self.last_changed = last_changed

  def to_json_dict(self):
    return {'v': self.value, 't': self.last_changed.strftime('%Y-%m-%dT%H:%M:%S')}

  @staticmethod
  def from_json_dict(username, label):
    last_changed = datetime.datetime.strptime(label['t'], '%Y-%m-%dT%H:%M:%S')
    return Label(username, label['v'], last_changed)
