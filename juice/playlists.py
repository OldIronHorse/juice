from urllib.parse import unquote
import juice.message.format as msg_format
from juice.message.parse import parse_msg

def get_status(server, player_id):
  request = msg_format.player_status(player_id, start=0, page_size=9999);
  server.write(request.encode('ascii'))
  response = server.read_until(b'\n')
  msg = parse_msg(response.decode('ascii'))
  return msg

def playlist_from_player_status(status):
  return [{k: v for k, v in track.items() if k in ['title','artist','album']}
          for track in status['player']['playlist']]

def get_current_playlist(server, player_id):
  return playlist_from_player_status(get_status(server, player_id))

def get_playing_track(server,player_id):
  status = get_status(server, player_id)
  playlist = playlist_from_player_status(status)
  return playlist[status['player']['playlist_cur_index']]
