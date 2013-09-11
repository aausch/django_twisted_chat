import time

from twisted.protocols import basic


class WebsocketChat(basic.LineReceiver):
    def connectionMade(self):
        print "Got new client!"
        self.transport.write('connected ....\n')
        self.factory.clients.append(self)

    def connectionLost(self, reason):
        print "Lost a client!"
        self.factory.clients.remove(self)

    def dataReceived(self, data):
        self.factory.messages[float(time.time())] = data
        self.updateClients(data)

    def updateClients(self, data):
        for c in self.factory.clients:
            c.message(data)

    def message(self, message):
        self.transport.write(message + '\n')
