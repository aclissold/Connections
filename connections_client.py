#!/usr/bin/env python3
import os
import socket
import threading

HOST = 'localhost'
PORT = 50007

player = int(input("Player 1 or 2: "))
#os.system('clear')

class SendThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        if player == 1:
            # X's
            while True:
                msg = "1" + input()
                msg = bytes(msg, 'ascii')
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((HOST, PORT))
                s.sendall(msg)
                s.close()
        elif player == 2:
            # O's
            while True:
                msg = "2" + input()
                msg = bytes(msg, 'ascii')
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((HOST, PORT))
                s.sendall(msg)
                s.close()
        else:
            raise Exception("You must enter a 1 or 2.")

class RecvThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        if player == 1:
            # X's
            while True:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((HOST, PORT))
                s.sendall(b'3')
                data = (s.recv(1024))
                if data != b'':
                    data = str(data, 'utf-8')
                    print(data)
                s.close()
        elif player == 2:
            # O's
            while True:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((HOST, PORT))
                s.sendall(b'0')
                data = s.recv(1024)
                if data != b'':
                    data = str(data, 'utf-8')
                    print(data)
                s.close()
        else:
            raise Exception("You must enter a 1 or 2.")

sendThread = SendThread()
recvThread = RecvThread()

sendThread.start()
recvThread.start()
