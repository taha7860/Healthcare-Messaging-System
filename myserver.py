import sys
from ex2utils import Server

class MyServer(Server):
    num_clients = 0
    
    def onStart(self):
        self.printOutput('My server has started')

    def onStop(self):
        self.printOutput('My server has stopped')

    def onConnect(self, socket):
        MyServer.num_clients += 1
        self.printOutput('new client connected')
        self.printOutput(f'{MyServer.num_clients} active clients')

    def onDisconnect(self, socket):
        MyServer.num_clients -= 1
        self.printOutput('a client disconnected')
        self.printOutput(f'{MyServer.num_clients} active clients')

    def onMessage(self, socket, message):
        message = message.encode()
        socket.send(message)

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
