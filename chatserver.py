from twisted.protocols import basic
from twisted.web.websockets import WebSocketsResource, WebSocketsProtocol, lookupProtocolForFactory

import time, datetime, json, thread
from twisted.web.resource import Resource
from twisted.internet import task
from twisted.web.server import NOT_DONE_YET

write_lock = thread.allocate_lock() #forcing synchronized writes between the various kinds of clients

class WebsocketChat(basic.LineReceiver):

    def connectionMade(self):
        print "Got new client!"
	self.transport.write('connected ....\n')
	self.factory.clients.append(self)
    
    def connectionLost(self, reason):
        print "Lost a client!"
	self.factory.clients.remove(self)
    

    def dataReceived(self, data):
        write_lock.acquire()
        self.factory.messages[float(time.time())] = data
        write_lock.release()
        self.updateClients(data)

    def updateClients(self, data):
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
    protocol = WebsocketChat
    clients = []
    messages = {}

class HttpChat(Resource):
    #optimization 
    isLeaf = True
    def __init__(self):
        # throttle in seconds to check app for new data
        self.throttle = 1
        # define a list to store client requests
        self.delayed_requests = []
        self.messages = {}
 
        #instantiate a ChatFactory, for generating the websocket protocols
        self.wsFactory = ChatFactory()
 
        # setup a loop to process delayed requests
        # not strictly neccessary, but a useful optimization, 
        # since it can force dropped connections to close, etc...
        loopingCall = task.LoopingCall(self.processDelayedRequests)
        loopingCall.start(self.throttle, False)
 
        #share the list of messages between the factories of the two protocols
        write_lock.acquire()
        self.wsFactory.messages = self.messages
        write_lock.release()
        # initialize parent
        Resource.__init__(self)
 
    def render_POST(self, request):
        request.setHeader('Content-Type', 'application/json')
        args = request.args
        if 'new_message' in args:
            write_lock.acquire()
            self.messages[float(time.time())] = args['new_message'][0]
            write_lock.release()
            if len(self.wsFactory.clients) > 0:
                self.wsFactory.clients[0].updateClients(args['new_message'][0])
            self.processDelayedRequests()
        return ''
 
    def render_GET(self, request):
        request.setHeader('Content-Type', 'application/json')
        args = request.args
                
        if 'callback' in args:
            request.jsonpcallback =  args['callback'][0]
         
        if 'lastupdate' in args:
            request.lastupdate =  float(args['lastupdate'][0])
        else:
            request.lastupdate = 0.0
 
        if request.lastupdate < 0:             
            return self.__format_response(request, 1, "connected...", timestamp=0.0)         
 
        #get the next message for this user
        data = self.getData(request)         
        if data:             
            return self.__format_response(request, 1, data.message, timestamp=data.published_at)
 
        self.delayed_requests.append(request)         
        return NOT_DONE_YET             
 
    #returns the next sequential message, 
    #and the time it was received at
    def getData(self, request):         
        for published_at in sorted(self.messages):               
            if published_at > request.lastupdate:
                return type('obj', (object,), {'published_at' : published_at, "message": self.messages[published_at]})(); 
        return
       
    def processDelayedRequests(self):
        for request in self.delayed_requests:
            data = self.getData(request)
           
            if data:
                try:
                    request.write(self.__format_response(request, 1, data.message, data.published_at))
                    request.finish()
                except:
                    print 'connection lost before complete.'
                finally:
                    self.delayed_requests.remove(request)
 
    def __format_response(self, request, status, data, timestamp=float(time.time())):
        response = json.dumps({'status':status,'timestamp': timestamp, 'data':data})
       
        if hasattr(request, 'jsonpcallback'):
            return request.jsonpcallback+'('+response+')'
        else:
            return response

from twisted.web.resource import Resource
from twisted.web.server import Site
 
from twisted.internet import protocol
from twisted.application import service, internet
 
resource = HttpChat()
factory = Site(resource)
ws_resource = WebSocketsResource(lookupProtocolForFactory(resource.wsFactory))
root = Resource()
root.putChild("",resource) #the http protocol is up at /
root.putChild("ws",ws_resource) #the websocket protocol is at /ws
application = service.Application("chatserver")
internet.TCPServer(1025, Site(root)).setServiceParent(application)
