from telnetlib import Telnet

def connect(host,port=9090):
  return Telnet(host,port)
