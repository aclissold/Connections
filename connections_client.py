#!/usr/bin/env python3
import socket

HOST = 'localhost'
PORT = 50007

# X's
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall(b'xHello, world')
data = s.recv(1024)
s.close()
print(data.decode('utf-8'))

# O's
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall(b'oHello, world')
data = s.recv(1024)
s.close()
print(data.decode('utf-8'))
