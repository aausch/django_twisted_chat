from twisted.internet.protocol import Factory

from twisted_chat.protocols import WebsocketChat


class ChatFactory(Factory):
    protocol = WebsocketChat
    clients = []
    messages = {}
