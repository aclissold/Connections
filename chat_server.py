#!/usr/bin/env python3

"""
A basic, multiclient 'chat server' using Python's select module
with interrupt handling.

Entering any line of input at the terminal will exit the server.
"""

import select
import socket
import sys
import signal
from communication import send, receive

SIZE = 1024


class ChatServer(object):
    """ Simple chat server using select """
    
    def __init__(self, port=50000, backlog=5):
        self.clients = 0
        # Client map
        self.clientmap = {}
        # Output socket list
        self.outputs = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('',port))
        print('Listening to port', port, '...')
        self.server.listen(backlog)

    def get_name(self, client):
        # Return the printable name of the
        # client, given its socket...
        info = self.clientmap[client]
        host, name = info[0][0], info[1]
        return '@'.join((name, host))
        
    def serve(self):
        inputs = [self.server,sys.stdin]
        self.outputs = []

        running = 1

        while running:

            inputready,outputready,exceptready = select.select(inputs,
                self.outputs, [])
            # except select.error, e:
            #     break
            # except socket.error, e:
            #     break

            for s in inputready:

                if s == self.server:
                    # handle the server socket
                    client, address = self.server.accept()
                    # only allow two clients
                    if self.clients > 1:
                        client.close()
                    else:
                        print('chatserver: got connection {} from {}'.format(
                            (client.fileno(), address)))
                        # Read the login name
                        cname = receive(client).split('NAME: ')[1]
                        
                        # Compute client name and send back
                        self.clients += 1
                        send(client, 'CLIENT: ' + str(address[0]))
                        inputs.append(client)

                        self.clientmap[client] = (address, cname)
                        # Send joining information to other clients
                        msg = '\n(Connected: New client ({}) from {})'.format(
                            (self.clients, self.get_name(client)))
                        for o in self.outputs:
                            # o.send(msg)
                            send(o, msg)
                        
                        self.outputs.append(client)

                elif s == sys.stdin:
                    # handle standard input
                    junk = sys.stdin.readline()
                    running = 0
                else:
                    # handle all other sockets
                    # try:
                        # data = s.recv(SIZE)
                        data = receive(s)
                        if data:
                            # Send as new client's message...
                            msg = '\n#[' + self.get_name(s) + ']>> ' + data
                            # Send data to all except ourselves
                            for o in self.outputs:
                                if o != s:
                                    send(o, msg)
                        else:
                            print('chatserver: {} hung up'.format(fileno()))
                            self.clients -= 1
                            s.close()
                            inputs.remove(s)
                            self.outputs.remove(s)

                            # Send client leaving information to others
                            msg = '\n(Hung up: Client from {})'.format(
                                self.get_name(s))
                            for o in self.outputs:
                                send(o, msg)
                                
                    # except socket.error, e:
                    #     # Remove
                    #     inputs.remove(s)
                    #     self.outputs.remove(s)

        self.server.close()


if __name__ == "__main__":
    ChatServer().serve()
