"""
How to Install, Run, and Test the IRC Messaging System

Installation:
1. Ensure Python 3 is installed.
2. Place the following files in the same directory:
   - ex2utils.py (provided utility module)
   - myserver.py (my server implementation)
   - myclient.py (my client implementation)
   - commands.json (protocol commands)

Running:
- Start the server: `python3 myserver.py <IP> <PORT>`
  Example: `python3 myserver.py localhost 8090`
- Start the client: `python3 myclient.py <IP> <PORT>`
  Example: `python3 myclient.py localhost 8090`

Testing:
1. **Register:** Enter a username when prompted.
   - Example: `alice` → Server: `register alice`
   If username taken or is more than one word, prompted again.
2. **Send to all:** `send_all Hello everyone!`
   For this, start more clients and register with them.
   Sends message to every user that is registered.
3. **Send to one:** `send_one bob Hi Bob!`
   Sends message to specified user.
4. **Check online users:** `online_users`
   Asks you to prompt again if you type the command with a message.
5. **Invalid command:** `some_invalid_command` → Response: `Invalid command. Try again.`
6. **Close connection:** `close_connection`
   - Client: `Client exiting`
   - Server: `a client disconnected`
   Closes client console for specific client instance.
"""

import sys
from ex2utils import Client

import time

class MyClient(Client):
    registered = False
    
    def onMessage(self, socket, message):
        # message is what is sent by the server with socket.send()
        if message == 'invalid username':
            print('Username does not allow spaces, please try again.')
        elif message == 'user already registered':
            print('User already registered. Register with a new username.')
        elif message == 'invalid protocol' or message == 'unknown command':
            print('Invalid command. Try again.')
        else:
            MyClient.registered = True # allows termination of initial loop
            print('\n' + message)
        
        return True


# Parse the IP address and port you wish to connect to.
ip = sys.argv[1]
port = int(sys.argv[2])

# Create an IRC client.
client = MyClient()

# Start server
client.start(ip, port)

# loops until user is registered
while not MyClient.registered:
    username = input('Enter your username: ')
    client.send(b'register ' + username.encode()) # sends command to the server

while True:
    command = input('Enter your command: ')
    client.send(command.encode())
    
    if command == 'close_connection': # terminates loop when the client's connection to the server is closed
        break

#stops client
client.stop()
