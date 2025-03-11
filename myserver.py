import sys
from ex2utils import Server

class MyServer(Server):
    def onStart(self):
        self.num_clients = 0
        self.users = {}
        self.printOutput('My server has started')

    def onStop(self):
        self.printOutput('My server has stopped')

    def onConnect(self, socket):
        socket.username = None
        self.num_clients += 1
        self.printOutput('new client connected')
        self.printOutput(f'{self.num_clients} active clients')

    def onDisconnect(self, socket):
        self.num_clients -= 1
        self.printOutput('a client disconnected')
        self.printOutput(f'{self.num_clients} active clients')
        del self.users[socket.username]

    def onMessage(self, socket, message):
        self.printOutput(message)

        if message.strip() == '':
            self.printOutput('Received empty message.')
            return True

        message_split = message.split()
        command = message_split[0]
        params = message_split[1:]
        self.printOutput(f'Command: {command}')
        self.printOutput(f'Params: {params}')

        if command == 'register':
            self.register(params, socket)
        elif command == 'send_all':
            self.send_all(params, socket)
        elif command == 'send_one':
            self.send_one(params, socket)
        elif command == 'online_users':
            self.online_users(params, socket)
        elif command == 'close_connection':
            self.close_connection(params, socket)
        else:
            socket.send(b'unknown command')

        return True
    
    def register(self, user, socket):
        if len(user) == 0 or len(user) > 1:
            socket.send(b'Invalid protocol')
            return True
        if user[0] in self.users:
            socket.send(b'user already registered')
            return True
        
        socket.username = user[0]
        socket.send(b'registered successfully')
        self.users[socket.username] = socket
        return True

    def send_all(self, text, socket):
        if not text:
            socket.send(b'Invalid protocol')
            return True
        
        msg = ' '.join(text)
        socket.send(b'Your message: ' + msg.encode())
        for user, r_socket in self.users.items():
            if user != socket.username:
                r_socket.send(b'message from ' + self.username.encode() + b': ' + msg.encode())
        return True

    def send_one(self, params, socket):
        if len(params) <= 1:
            socket.send(b'Invalid protocol')
            return True
        elif params[0] not in self.users:
            socket.send(b'not registered')
            return True
        
        recipient = params[0]
        msg = ' '.join(params[1:])

        socket.send(b'Your message: ' + msg.encode())
        self.users[recipient].send(b'message from ' + self.username.encode() + b': ' + msg.encode())
        return True

    def online_users(self, params, socket):
        if params:
            socket.send(b'Invalid protocol')
            return True

        socket.send(b'users online:' + ', '.join(self.users).encode())
        return True

    def close_connection(self, params, socket):
        if params:
            socket.send(b'Invalid protocol')
            return True




# Parse the IP address and port you wish to listen on.
ip = sys.argv[1]
port = int(sys.argv[2])

# Create an echo server.
server = MyServer()

# If you want to be an egomaniac, comment out the above command, and uncomment the
# one below...
# server = EgoServer()

# Start server
server.start(ip, port)
