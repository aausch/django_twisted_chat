import json
import time

from twisted.internet import task

from twisted.web.resource import Resource
from twisted.web.static import File
from twisted.web.server import NOT_DONE_YET

from twisted_chat.factories import ChatFactory


class HttpChat(Resource):
    #optimization 
    isLeaf = True
    messages = {}
    def __init__(self, messages = None):
        # throttle in seconds to check app for new data
        self.throttle = 1
        # define a list to store client requests
        self.delayed_requests = []
        if messages:
            self.messages = messages
 
        #instantiate a ChatFactory, for generating the websocket protocols
        self.wsFactory = ChatFactory()
 
        # setup a loop to process delayed requests
        # not strictly neccessary, but a useful optimization, 
        # since it can force dropped connections to close, etc...
        loopingCall = task.LoopingCall(self.processDelayedRequests)
        loopingCall.start(self.throttle, False)
 
        #share the list of messages between the factories of the two protocols
        self.wsFactory.messages = self.messages
        # initialize parent
        Resource.__init__(self)
 
    def render_POST(self, request):
        request.setHeader('Content-Type', 'application/json')
        args = request.args
        if 'new_message' in args:
            self.messages[float(time.time())] = args['new_message'][0]
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
                return type('obj', (object,), {
                        'published_at' : published_at,
                              "message": self.messages[published_at]
                        })(); 
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
        
        
class StaticFileScanner(Resource):
    dirs = []
    def __init__(self, *dirs):
        if (len(dirs) < 1):
            self.dirs = [File()]
        else:
            self.dirs = [File(d) for d in dirs]
        Resource.__init__(self)
    
    def getChild(self, *args):
        for d in self.dirs:
            if d.getChild(*args) != d.childNotFound:
                return d.getChild(*args)
        return self.dirs[0].childNotFound
    
