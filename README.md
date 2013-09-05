**Partially implemented chat server.**



(An experiment in using twisted with websockets, with a site served by Django.)

(Django serves the static/http pages, by default on port 8000 on localhost, while twisted handles the chat server, by default on port 1025 on localhost)


**STARTUP INSTRUCTIONS**


* Start this as a standard django project (./manage.py runserver) 
  * don't forget to do fun things like syncdb before starting
* Create a chat room through django's admin interface (localhost:8080/admin/)
* "twistd -y chatserver.py", though probably "twistd -n -y chatserver.py" is more appropriate since you're likely not going to use this for production at any time

To see the chat service in action: 
* a list of existing chat rooms is at localhost:8000/chats
* chat over websockets at localhost:8000/chats/[room_id]
* chat over HTTP, with a long-polling service, at localhost:8000/chats/long_poll/[room_id]

**DEPENDENCIES**

Note that I'm relying on the websockets branch (I used [websocket-4173-4](https://github.com/twisted/twisted/tree/websocket-4173-4)) of twisted, so make sure to install that (I don't think it's merged into the main branch yet)   

See requirements.txt for versions of dependencies. 

I've been running things in a standard python2.7 virtualenv, with pip for package management

**TODO:**
 * Integrate twisted and django authentication
 * have twisted log chats to django's database
 * nice ui for creating chat rooms, etc....
