
class InvalidMsgException(Exception):
  pass


def parse_login(msg):
  try:
    command, user, stars = msg.split(' ')
    if '******' != stars:
      raise InvalidMsgException
    return {'command': command, 'user': user}
  except ValueError:
    raise InvalidMsgException

def parse_listen(msg):
  try:
    command, value = msg.split(' ')
    value = int(value)
    if value not in [0,1]:
      raise InvalidMsgException
    return {'command': command, 'value': value}
  except ValueError:
    raise InvalidMsgException

def parse_subscribe(msg):
  command, notifications = msg.split(' ')
  return {'command':command, 'notifications': notifications.split(',')}

cmd_parsers = {
  'login': parse_login,
  'listen': parse_listen,
  'subscribe': parse_subscribe,
  }

def parse_msg(msg):
  cmd, _ = msg.split(' ', 1)
  try:
    return cmd_parsers[cmd](msg)
  except KeyError:
    raise InvalidMsgException

