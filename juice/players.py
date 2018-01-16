from urllib.parse import unquote
import juice.message.format as msg_format
from juice.message.parse import parse_msg

#TODO: remove named tuples
#TODO: refactor to use msg_format and parse_msg

def indexed_query(server,obj,prop,index):
  server.write('{} {} {} ?\n'.format(obj,prop,index).encode('ascii'))
  
  response = server.read_until(b'\n').decode('ascii').split()
  try:
    if response[0] == obj and \
       response[1] == prop and \
       unquote(response[2]) == str(index):
      return unquote(response[3])
  except AttributeError:
    raise IndexError

def get_player_name(server, index):
  return indexed_query(server,'player','name',index)

def get_player_count(server):
  server.write(b'player count ?\n')
  response = server.read_until(b'\n').decode('ascii').split()
  if response[0] == 'player' and \
     response[1] == 'count':
    return int(response[2])
  
def get_player_id(server,index):
  return indexed_query(server,'player','id',index)

def get_players(server):
  players = []
  for i in range(0,get_player_count(server)):
    players.append({'index': i,
                    'name': get_player_name(server,i),
                    'id': get_player_id(server,i)})
  return players

def play(server, id):
  server.write('{} play\n'.format(id).encode('ascii'))
  response = server.read_until(b'\n').decode('ascii').split()

def pause(server, id):
  server.write('{} pause\n'.format(id).encode('ascii'))
  response = server.read_until(b'\n').decode('ascii').split()

def state(server, id):
  server.write('{} mode ?\n'.format(id).encode('ascii'))
  response = server.read_until(b'\n').decode('ascii').split()
  if response[2] not in ['play','pause','stop']:
    raise ValueError
  return response[2]

def get_player_volume(server, id):
  server.write('{} mixer volume ?\n'.format(id).encode('ascii'))
  return int(server.read_until(b'\n').decode('ascii').split()[3])

def set_player_volume(server, id, vol):
  server.write('{} mixer volume {}\n'.format(id, vol).encode('ascii'))
  server.read_until(b'\n')

def next_track(server, player_id):
  server.write(msg_format.next_track(player_id).encode('ascii'))
  server.read_until(b'\n')

def previous_track(server, player_id):
  server.write(msg_format.previous_track(player_id).encode('ascii'))
  server.read_until(b'\n')
