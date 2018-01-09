from urllib.parse import unquote

class InvalidMsgException(Exception):
  pass

def try_int(s):
  try:
    return int(s)
  except ValueError:
    return s

def try_numeric(s):
  try:
    return int(s)
  except ValueError:
    try:
      return float(s)
    except ValueError:
      return s

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
  value = unquote(value)
  reply = {'id': unquote(player_id)}
  if cmd == 'mixer':
    cmd, value = value.split(' ', 1)
    if value.startswith('-') or value.startswith('+'):
      cmd += '_change'
  reply[cmd] = try_numeric(value)
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

def parse_players(msg):
  cmd, start, max_count, player_count, fields = msg.split(' ', 4)
  _, player_count = unquote(player_count).split(':',1)
  players = []
  for field in fields.split(' '):
    k, v = unquote(field).split(':',1)
    try:
      if k not in ['firmware']:
        v = int(v)
    except ValueError:
      pass
    if k == 'playerindex':
      player = {'index': v}
      players.append(player)
    elif k == 'playerid':
      player['id'] = v
    else:
      player[k] = v
  return {'player_count': int(player_count), 'players': players}

def parse_total_genres(msg):
  return {'genre_count': int(msg)}

def parse_total_artists(msg):
  return {'artist_count': int(msg)}

def parse_total_albums(msg):
  return {'album_count': int(msg)}

def parse_total_songs(msg):
  return {'song_count': int(msg)}

def parse_total_duration(msg):
  return {'total_duration': int(msg)}

info_subparsers = {
  'total': {
    'genres': parse_total_genres,
    'artists': parse_total_artists,
    'albums': parse_total_albums,
    'songs': parse_total_songs,
    'duration': parse_total_duration,
    },
  }

def parse_info(msg):
  cmd, subcmd, category, rest = msg.split(' ', 3)
  return info_subparsers[subcmd][category](rest)

def parse_library(msg):
  cmd, start, page_size, rest = msg.split(' ', 3)
  reply = {'start': int(start), 'page_size': int(page_size)}
  fields = rest.split(' ')
  result_list = []
  result_type = cmd[0:-1]
  reply[cmd] = result_list
  parsing_list = False;
  for field in fields:
    k, v = unquote(field).split(':', 1)
    if k == 'id':
      parsing_list = True
    if parsing_list:
      if k == 'id':
        result_list.append({k: int(v)})
      elif k == result_type:
        result_list[-1]['name'] = v
      elif k == 'count':
          reply[k] = int(v)
      else:
        result_list[-1][k] = try_numeric(v)
    else:
      reply[k] = try_int(v)
  return reply

def parse_years(msg):
  cmd, start, page_size, fields = msg.split(' ', 3)
  years = []
  reply = {
    'start': int(start),
    'page_size': int(page_size),
    'years' : years,
    }
  for field in fields.split(' '):
    k, v = unquote(field).split(':', 1)
    if k == 'year':
      years.append(int(v))
    else:
      reply[k] = try_int(v)
  return reply

def parse_search(msg):
  cmd, start, page_size, term, results = msg.split(' ', 4)
  reply = {
    'start': int(start), 
    'page_size': int(page_size),
    'contributors': [],
    'albums': [],
    'tracks': [],
  }
  term_tag, term_value = unquote(term).split(':', 1)
  reply['term'] = term_value
  for result in results.split(' '):
    k, v = unquote(result).split(':', 1)
    if k == 'term':
      reply[k] = v
    if k in ['count', 'contributors_count', 'albums_count', 'tracks_count']:
      reply[k] = int(v)
    else:
      try:
        key_type, key_value = k.split('_')
      except ValueError:
        key_type = k
        key_value = 'name'
      key_type += 's'
      if key_value == 'id':
        reply[key_type].append({'id': int(v)})
      else:
        reply[key_type][-1][key_value] = v
  return reply

cmd_parsers = {
  'login': parse_login,
  'listen': parse_listen,
  'subscribe': parse_subscribe,
  'player' : parse_player,
  'players' : parse_players,
  'syncgroups': parse_syncgroups,
  'info': parse_info,
  'genres': parse_library,
  'artists': parse_library,
  'albums': parse_library,
  'years': parse_years,
  'tracks': parse_library,
  'search': parse_search,
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
