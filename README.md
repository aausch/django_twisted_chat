An experiment in using twisted with websockets, with a site served by Django.

Partially implemented chat server.

Django serves the static/http pages, by default on port 8000 on localhost, while twisted handles the chat server, by default on port 1025 on localhost

TODO:
 * Integrate twisted and django authentication
 * have twisted log chats to django's database
 * nice ui for creating chat rooms, etc....

Start this as a standard django project - don't forget to do fun things like syncdb

Make sure to create a chat room through django's admin interface (localhost:8080/admin/)

Note that I'm relying on the websockets branch of twisted, so make sure to install that (I don't think it's merged into the main branch yet)

Start the twisted chat app with something like "twistd -y chatserver.py"

To see the chat service in action: 
* a list of existing chat rooms is at localhost:8000/chats
* chat over websockets at localhost:8000/chats/<room_id>
* chat over HTTP, with a long-polling service, at localhost:8000/chats/long_poll/<room_id>

