from collections import namedtuple
from telnetlib import Telnet
from urllib.parse import unquote

PlayerMessage = namedtuple('PlayerMessage',
                           'player_id name msg_type start per_page tags')

def connect(host,port=9090):
  return Telnet(host,port)

def listen(server):
  server.write(b'listen 1\n')

def subscribe_status(server, player_id):
  server.write('{} status - 2 subscribe:30\n'.format(player_id).encode('ascii'))

def read_loop(server, onMessage):
  while(True):
    msg = server.read_until(b'\n').decode('ascii').split(' ')
    fields = [unquote(field) for field in msg]
    onMessage(PlayerMessage(fields[0], fields[1], fields[2], fields[3], fields[4],
              {t: v for [t,v] in [field.split(':',1) for field in fields[5:]]}))
