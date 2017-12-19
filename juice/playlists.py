from urllib.parse import unquote
from collections import namedtuple

Track = namedtuple('Track', 'track album artist')

def get_current_playlist(server,player_id):
  server.write('{} status 0 9999 tags:la\n'.format(player_id).encode('ascii'))
  response = server.read_until(b'\n').decode('ascii').split()
  response = [unquote(tag).split(':',1) for tag in response]
  playlist = []
  track = {}
  for tag in response:
    if tag[0] in ['title','album','artist']:
      if tag[0] in track:
        playlist.append(Track(track['title'],track.get('album',None),track['artist']))
        track = {}
      track[tag[0]] = tag[1]
  if track:
    playlist.append(Track(track['title'],track.get('album',None),track['artist']))
  return playlist

def get_playing(server,player_id,field):
  server.write('{} {} ?\n'.format(player_id, field).encode('ascii'))
  response = server.read_until(b'\n').decode('ascii').split()
  try:
    return unquote(response[2])
  except IndexError:
    return None

def get_playing_title(server,player_id):
  return get_playing(server,player_id,'title')

def get_playing_album(server,player_id):
  return get_playing(server,player_id,'album')

def get_playing_artist(server,player_id):
  return get_playing(server,player_id,'artist')

def get_playing_track(server,player_id):
  return Track(get_playing_title(server,player_id),
               get_playing_album(server,player_id),
               get_playing_artist(server,player_id))
