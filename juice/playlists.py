from urllib.parse import unquote

def get_playing(server,player_id,field):
  server.write('{} {} ?\n'.format(player_id, field).encode('ascii'))
  response = server.read_until(b'\n').decode('ascii').split(' ')
  return unquote(response[2])

def get_playing_title(server,player_id):
  return get_playing(server,player_id,'title')

def get_playing_album(server,player_id):
  return get_playing(server,player_id,'album')

def get_playing_artist(server,player_id):
  return get_playing(server,player_id,'artist')
