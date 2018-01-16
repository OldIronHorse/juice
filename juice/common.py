from telnetlib import Telnet
from urllib.parse import unquote
from juice.message.parse import parse_msg
from threading import Thread

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

def read_worker(server, onMsg):
  while(True):
    msg = parse_msg(server.read_until(b'\n').decode('ascii'))
    onMsg(msg)

def loop_start(server, onMsg):
  Thread(target=read_worker, args=(server, onMsg)).start()
