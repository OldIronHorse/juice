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

def players(start=0, page_size=10):
  return 'players {} {}\n'.format(start, page_size)

def total(category):
  return 'info total {} ?\n'.format(category)

def category_query(category, start, page_size, filtres):
  msg = '{} {} {} tags:lytiqwaSesucj'.format(category, start, page_size)
  for k in sorted(filtres.keys()):
    msg += ' {}:{}'.format(k, filtres[k])
  return msg + '\n'

def genres(start=0, page_size=100, **kwargs):
  return category_query('genres', start, page_size, kwargs)

def artists(start=0, page_size=100, **kwargs):
  return category_query('artists', start, page_size, kwargs)

def albums(start=0, page_size=100, **kwargs):
  return category_query('albums', start, page_size, kwargs)

def years(start=0, page_size=100, **kwargs):
  return category_query('years', start, page_size, kwargs)

def tracks(start=0, page_size=100, **kwargs):
  return category_query('tracks', start, page_size, kwargs)

def player_status(player_id, start='-', page_size=100, subscribe=None):
  msg = '{} status {} {} tags:ales'.format(player_id, start, page_size)
  if subscribe is None:
    msg += '\n'
  else:
    msg += ' subscribe:{}\n'.format(subscribe)
  return msg

def next_track(player_id):
  return player_by_id(player_id, 'playlist index', '+1')

def previous_track(player_id):
  return player_by_id(player_id, 'playlist index', '-1')

def player_playlist_control(player_id, cmd, **kwargs):
  msg = '{} playlistcontrol cmd:{}'.format(player_id, cmd)
  print(msg)
  for k in kwargs.keys():
    msg += ' {}:{}'.format(k, kwargs[k])
  print(msg)
  return msg +'\n'

def player_playlist_delete(player_id, index):
  return '{} playlist delete {}\n'.format(player_id, index)
