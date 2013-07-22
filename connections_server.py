#!/usr/bin/env python3
# Test server

import socket
import threading
import socketserver

newMessage1 = newMessage2 = False
data1 = data2 = bytes("test", "ascii")

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = str(self.request.recv(1024), 'ascii')
        global data1, data2
        if data[0] == '0':
            global newMessage1
            if newMessage1:
                self.request.sendall(data1)
                newMessage1 = False
            else:
                while not newMessage1:
                    if newMessage1:
                        self.request.sendall(data1)
                        newMessage1 = False
        elif data[0] == '3':
            global newMessage2
            if newMessage2:
                self.request.sendall(data2)
                newMessage2 = False
            else:
                while not newMessage1:
                    if newMessage2:
                        self.request.sendall(data2)
                        newMessage2 = False
        elif data[0] == '1':
            data1 = bytes("Rachel: " + data[1:], 'ascii')
            newMessage1 = True
        elif data[0] == '2':
            data2 = bytes("Andrew: " + data[1:], 'ascii')
            newMessage2 = True
        else:
            raise Exception("Erroneous data received.")

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST = ''
    PORT = 50007
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    while True:
        pass
