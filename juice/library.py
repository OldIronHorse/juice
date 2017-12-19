from collections import namedtuple
from urllib.parse import unquote

Artist = namedtuple('Artist','name id')

def get_artists(server):
  server.write(b'artists 0 9999\n')
  response = server.read_until(b'\n').decode('ascii').split()
  response = [unquote(tag).split(':',1) for tag in response[3:]]
  artists = []
  artist = {}
  for tag, value in response:
    if tag in ['id','artist']:
      if tag in artist:
        artists.append(Artist(artist['artist'],int(artist['id'])))
        artist = {}
      artist[tag] = value
  artists.append(Artist(artist['artist'],int(artist['id'])))
  return artists
