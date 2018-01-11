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
