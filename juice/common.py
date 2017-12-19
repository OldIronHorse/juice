from telnetlib import Telnet

def connect(host,port):
  return Telnet(host,port)
