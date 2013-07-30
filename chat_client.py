#! /usr/bin/env python3

"""
Simple chat client for the chat server. Defines
a simple protocol to be used with chatserver.

"""

import socket
import sys
import select
from communication import send, receive

SIZE = 1024

class ChatClient(object):
    """ A simple command line chat client using select """

    def __init__(self, name, host='127.0.0.1', port=50000):
        self.name = name
        # Quit flag
        self.flag = False
        self.port = port
        self.host = host
        # Initial prompt
        self.prompt='[' + '@'.join((name,
            socket.gethostname().split('.')[0])) + ']> '
        # Connect to server at port
        # try:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, self.port))
        print('Established connection with server on port {}.'.format(self.port))
        # Send my name...
        send(self.sock, 'NAME: ' + self.name) 
        data = receive(self.sock)
        # Contains client address, set it
        addr = data.split('CLIENT: ')[1]
        self.prompt = '[' + '@'.join((self.name, addr)) + ']> '
        # except socket.error, e:
        #     print 'Could not connect to chat server @%d' % self.port
        #     sys.exit(1)

    def cmdloop(self):
        while not self.flag:
            try:
                sys.stdout.write(self.prompt)
                sys.stdout.flush()

                # Wait for input from stdin & socket
                inputready, outputready, exceptready = select.select([0, self.sock],
                    [],[])

                for i in inputready:
                    if i == 0:
                        data = sys.stdin.readline().strip()
                        if data: send(self.sock, data)
                    elif i == self.sock:
                        data = receive(self.sock)
                        if not data:
                            print('Shutting down.')
                            self.flag = True
                            break
                        else:
                            sys.stdout.write(data + '\n')
                            sys.stdout.flush()
                                
            except KeyboardInterrupt:
                print('\nClosing socket.')
                self.sock.close()
                break

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit('Usage: {} name host port'.format(sys.argv[0]))
        
    client = ChatClient(sys.argv[1],sys.argv[2], int(sys.argv[3]))
    client.cmdloop()
