import os
from twisted.web.resource import Resource

os.environ['DJANGO_SETTINGS_MODULE'] = 'django_twisted_chat.settings'

class WsgiRoot(Resource):

    def __init__(self, wsgi_resource):
        Resource.__init__(self)
        self.wsgi_resource = wsgi_resource

    def getChild(self, path, request):
        path0 = request.prepath.pop(0)
        request.postpath.insert(0, path0)
        return self.wsgi_resource
