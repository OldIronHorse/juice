from collections import namedtuple
from urllib.parse import unquote
from .message.parse import parse_msg
from .message import format as msg_format

Artist = namedtuple('Artist','name id')

def get_artists(server, page_size=9999, **kwargs):
  request = msg_format.artists(page_size=page_size, **kwargs)
  #print('get_artists: request=', request)
  server.write(request.encode('ascii'))
  reply = server.read_until(b'\n').decode('ascii')
  #pirint('get_artists: reply=', reply)
  artists = parse_msg(reply)['artists']
  return artists

def get_albums(server, page_size=9999, **kwargs):
  request = msg_format.albums(page_size=page_size, **kwargs)
  server.write(request.encode('ascii'))
  reply = server.read_until(b'\n').decode('ascii')
  albums = parse_msg(reply)['albums']
  return albums

def get_tracks(server, **kwargs):
  request = msg_format.tracks(**kwargs)
  server.write(request.encode('ascii'))
  reply = server.read_until(b'\n').decode('ascii')
  tracks = parse_msg(reply)['tracks']
  return tracks

def get_genres(server, **kwargs):
  request = msg_format.genres(**kwargs)
  #print(request)
  server.write(request.encode('ascii'))
  reply = server.read_until(b'\n').decode('ascii')
  #print(reply)
  genres = parse_msg(reply)['genres']
  #print(genres)
  return genres

def get_years(server, page_size=9999, **kwargs):
  request = msg_format.years(page_size=page_size, **kwargs)
  server.write(request.encode('ascii'))
  reply = server.read_until(b'\n').decode('ascii')
  years = parse_msg(reply)['years']
  return years
  
