from collections import namedtuple
from urllib.parse import unquote

Player = namedtuple('Player','index name id')

def indexed_query(server,obj,prop,index):
  server.write('{} {} {} ?\n'.format(obj,prop,index).encode('ascii'))
  
  response = server.read_until(b'\n').decode('ascii').split()
  try:
    if response[0] == obj and \
       response[1] == prop and \
       int(response[2]) == index:
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
    players.append(Player(i,get_player_name(server,i),get_player_id(server,i)))
  return players
