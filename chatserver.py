from twisted.web.websockets import WebSocketsResource, WebSocketsProtocol, lookupProtocolForFactory
from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.internet import protocol
from twisted.application import service, internet

from twisted_chat.factories import ChatFactory
from twisted_chat.resources import HttpChat


shared_messages = {}

resource = HttpChat(shared_messages)
factory = Site(resource)
ws_resource = WebSocketsResource(lookupProtocolForFactory(resource.wsFactory))

root = Resource()
root.putChild("",resource) #the http protocol is up at /
root.putChild("ws",ws_resource) #the websocket protocol is at /ws

application = service.Application("chatserver")
internet.TCPServer(1025, Site(root)).setServiceParent(application)
