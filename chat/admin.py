from django.contrib import admin
from chat.models import ChatRoom, Message

admin.site.register(ChatRoom)
admin.site.register(Message)
