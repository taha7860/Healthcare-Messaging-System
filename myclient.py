"""

IRC client exemplar.

"""

import sys
from ex2utils import Client

import time

class MyClient(Client):
    
    def onMessage(self, socket, message):
        if message == 'invalid username':
            username = input('Something went wrong, please try again: ')
            socket.send(b'register ' + username.encode())
        elif message == 'user already registered':
            username = input('User already registered. Register with a new username: ')
            socket.send(b'register ' + username.encode())
        elif message == 'invalid protocol' or message == 'unknown command':
            command = input('Invalid command. Try again: ')
            socket.send(command.encode())
        else:
            print('\n' + message)
        
        return True


# Parse the IP address and port you wish to connect to.
ip = sys.argv[1]
port = int(sys.argv[2])

# Create an IRC client.
client = MyClient()

# Start server
client.start(ip, port)

#send message to the server
username = input('Enter your username: ')
client.send(b'register ' + username.encode())

while True:
    command = input('Enter your command: ')
    client.send(command.encode())
    
    if command == 'close_connection':
        break

#stops client
client.stop()
