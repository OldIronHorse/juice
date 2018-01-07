from urllib.parse import unquote

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

def player_count_parser(cmd, subcmd, rest):
  return {'command': cmd, subcmd: int(rest)}

def player_indexed_parser(cmd, subcmd, rest):
  index, player_id = rest.split(' ')
  if subcmd in ['id', 'name']:
    player_id = unquote(player_id)
  try:
    return {'command': cmd, subcmd: player_id, 'index': int(index)}
  except ValueError:
    return {'command': cmd, subcmd: player_id, 'id': unquote(index)}
    
def player_indexed_number_parser(cmd, subcmd, rest):
  result = player_indexed_parser(cmd, subcmd, rest)
  result[subcmd] = int(result[subcmd])
  return result


player_subparsers = {
  'count': player_count_parser,
  'id': player_indexed_parser,
  'uuid': player_indexed_parser,
  'name': player_indexed_parser,
  'ip': player_indexed_parser,
  'model': player_indexed_parser,
  'isplayer': player_indexed_number_parser,
}

def parse_player(msg):
  cmd, subcmd, rest= msg.split(' ',2)
  return player_subparsers[subcmd](cmd, subcmd, rest)

def parse_id(msg):
  player_id, cmd, value = msg.split(' ',2)
  reply = {'id': unquote(player_id)}
  if cmd == 'mixer':
    cmd, value = value.split(' ')
    if value.startswith('-') or value.startswith('+'):
      cmd += '_change'
  try:
    reply[cmd] = int(value)
  except ValueError:
    try:
      reply[cmd] = float(value)
    except ValueError:
      reply[cmd] = unquote(value)
  return reply

def parse_syncgroups(msg):
  fields = msg.split(' ')
  cmd = fields[0]
  kvs = {k: v for k, v in [unquote(field).split(':',1) for field in fields[1:]]}
  try:
    return {
        'ids': unquote(kvs['sync_members']).split(','),
        'names': unquote(kvs['sync_member_names']).split(','),
      }
  except KeyError:
    return {'ids':[], 'names': []}

cmd_parsers = {
  'login': parse_login,
  'listen': parse_listen,
  'subscribe': parse_subscribe,
  'player' : parse_player,
  'syncgroups': parse_syncgroups,
}

def parse_msg(msg):
  cmd = msg.split(' ', 1)[0]
  try:
    return cmd_parsers[cmd](msg)
  except KeyError:
    try:
      return parse_id(msg)
    except ValueError:
      raise InvalidMsgException
