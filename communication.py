#!/usr/bin/env python3
import pickle
import socket
import struct
import sys
def send(channel, *args):
    buf = pickle.dumps(args)
    value = socket.htonl(len(buf))
    size = struct.pack('L', value)
    channel.send(size)
    try:
        channel.send(buf)
    except BrokenPipeError:
        # Hopefully this only happens when I think it will
        print('Error: Only two clients may connect to the server '
              'simultaneously.')
        print('Disconnecting.')
        sys.exit()

def receive(channel):
    size = struct.calcsize('L')
    size = channel.recv(size)
    try:
        size = socket.ntohl(struct.unpack('L', size)[0])
    except struct.error:
        return ''
    
    buf = ''

    while len(buf) < size:
        buf = channel.recv(size - len(buf))

    return pickle.loads(buf)[0]
