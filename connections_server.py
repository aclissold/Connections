#!/usr/bin/env python3
# Test server

import socket

HOST = ''
PORT = 50007
while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(1)
    conn, addr = sock.accept()
    while True:
        data = conn.recv(1024)
        if not data: break
        data = data.decode('utf-8')
        if data[0] == 'x':
            print("Received connection from Player 1")
        elif data[0] == 'o':
            print("Received connection from Player 2")
        else:
            raise Exception("Erroneous data received.")
        data = data[1:]
        data = bytes(data, 'ascii')
        conn.sendall(data)
    conn.close()
