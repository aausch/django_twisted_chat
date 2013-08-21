**Partially implemented chat server.**


(An experiment in using twisted with websockets, with a site served by Django.)



**STARTUP INSTRUCTIONS**


* Start this as a standard django project (./manage.py runserver) 
  * don't forget to do fun things like syncdb before starting
* Create a chat room through django's admin interface (localhost:8080/admin/)
* "twistd -y chatserver.py", though probably "twistd -n -y chatserver.py" is more appropriate since you're likely not going to use this for production at any time


**DEPENDENCIES**


Note that I'm relying on the websockets branch (I used [websocket-4173-4](https://github.com/twisted/twisted/tree/websocket-4173-4)) of twisted, so make sure to install that (I don't think it's merged into the main branch yet)   

See requirements.txt for versions of dependencies. 

I've been running things in a standard python2.7 virtualenv, with pip for package management

**TODO:**
 * Integrate twisted and django authentication
 * have twisted log chats to django's database
 * nice ui for creating chat rooms, etc....
