from django.db import models


from django.db import models

class ChatRoom(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
	return self.name

class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom)
    contents = models.CharField(max_length=200)
    posted_date = models.DateTimeField('date received')

    def __unicode__(self):
	return self.chat_room.name+ " - " + self.contents
