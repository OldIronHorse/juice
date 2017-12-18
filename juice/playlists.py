from urllib.parse import unquote

def get_playing_title(server,player_id):
  server.write('{} title ?\n'.format(player_id).encode('ascii'))
  response = server.read_until(b'\n').decode('ascii').split(' ')
  return unquote(response[2])
