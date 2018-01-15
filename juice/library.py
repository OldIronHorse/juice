from collections import namedtuple
from urllib.parse import unquote
from .message.parse import parse_msg
from .message import format as msg_format

Artist = namedtuple('Artist','name id')

def get_artists(server, **kwargs):
  request = msg_format.artists(**kwargs)
  server.write(request.encode('ascii'))
  reply = server.read_until(b'\n').decode('ascii')
  artists = parse_msg(reply)['artists']
  return artists

def get_albums(server, **kwargs):
  request = msg_format.albums(**kwargs)
  print(request)
  server.write(request.encode('ascii'))
  reply = server.read_until(b'\n').decode('ascii')
  print(reply)
  albums = parse_msg(reply)['albums']
  return albums

def get_tracks(server, **kwargs):
  request = msg_format.tracks(**kwargs)
  print(request)
  server.write(request.encode('ascii'))
  reply = server.read_until(b'\n').decode('ascii')
  print(reply)
  tracks = parse_msg(reply)['tracks']
  return tracks
