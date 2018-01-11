from urllib.parse import quote

def login(user, password):
  return 'login {} {}\n'.format(user, password)

def listen(enable='?'):
  if enable == '?':
    return 'listen ?\n'
  elif enable:
    return 'listen 1\n'
  else:
    return 'listen 0\n'

def subscribe(notifications=[]):
  if notifications:
    return 'subscribe {}\n'.format(','.join(notifications))
  else:
    return 'subscribe\n'

def player(field, index=None):
  if index is None:
    return 'player {} ?\n'.format(field)
  else:
    return 'player {} {} ?\n'.format(field, index)

def player_by_id(player_id, field, new_value='?'):
  if field in ['volume','muting']:
    field = 'mixer ' + field
  elif new_value != '?':
    new_value = quote(new_value)
  return '{} {} {}\n'.format(player_id, field, new_value)

def syncgroups():
  return 'syncgroups ?\n'
