"""The most basic chat protocol possible.

run me with twistd -y chatserver.py, and then connect with multiple
telnet clients to port 1025
"""

from twisted.protocols import basic
from twisted.web.websockets import WebSocketsResource, WebSocketsProtocol, lookupProtocolForFactory



class MyChat(basic.LineReceiver):
    def connectionMade(self):
        print "Got new client!"
	self.transport.write('connected ....\n')
	self.factory.clients.append(self)
    
    def connectionLost(self, reason):
        print "Lost a client!"
	self.factory.clients.remove(self)
    

    def dataReceived(self, data):
        print "received", repr(data)
        for c in self.factory.clients:
            c.message(data)

    def message(self, message):
        self.transport.write(message + '\n')


from twisted.web.resource import Resource
from twisted.web.server import Site


from twisted.internet import protocol
from twisted.application import service, internet


from twisted.internet.protocol import Factory
class ChatFactory(Factory):
    protocol = MyChat
    clients = []

resource = WebSocketsResource(lookupProtocolForFactory(ChatFactory()))
root = Resource()
root.putChild("",resource)


application = service.Application("chatserver")
internet.TCPServer(1025, Site(root)).setServiceParent(application)
