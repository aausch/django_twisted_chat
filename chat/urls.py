from django.conf.urls import patterns, url

from chat import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^(?P<chat_room_id>\d+)/$', views.chat_room, name='chat_room'),
        url(r'^long_poll/(?P<chat_room_id>\d+)/$', views.longpoll_chat_room, name='longpoll_chat_room'),
)
