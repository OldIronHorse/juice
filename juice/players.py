from re import fullmatch
from collections import namedtuple

Player = namedtuple('Player','index name id')

def indexed_query(server,obj,prop,index):
  server.write('{} {} {} ?\n'.format(obj,prop,index).encode('ascii'))
  response = fullmatch(r'([a-z]+) ([a-z]+) ([0-9]+) (.+)\n',
                       server.read_until(b'\n').decode('ascii'))
  try:
    if response.group(1) == obj and \
       response.group(2) == prop and \
       int(response.group(3)) == index:
      return response.group(4)
  except AttributeError:
    raise IndexError
  

def get_player_name(server, index):
  return indexed_query(server,'player','name',index)

def get_player_count(server):
  server.write(b'player count ?\n')
  response = server.read_until(b'\n').decode('ascii')
  print(response)
  return int(fullmatch(r'player count ([0-9]+)\n', response).group(1))
  
def get_player_id(server,index):
  return indexed_query(server,'player','id',index)

def get_players(server):
  players = []
  for i in range(0,get_player_count(server)):
    players.append(Player(i,get_player_name(server,i),get_player_id(server,i)))
  return players
