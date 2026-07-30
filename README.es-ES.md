

# 🚨🚨🚨 OBSOLETO/NO MANTENIDO 🚨🚨🚨
-


**Servidor de chat parcialmente implementado.**


(Un experimento usando Twisted con WebSockets, con un sitio alojado por Django.)

(Django sirve las páginas estáticas/HTTP, por defecto en el puerto 8000 de localhost, mientras que Twisted maneja el servidor de chat, por defecto en el puerto 1025 de localhost)


**INSTRUCCIONES DE EJECUCIÓN**


* Inicia este proyecto como un proyecto Django estándar (./manage.py runserver) 
  * no olvides realizar cosas divertidas como syncdb antes de iniciar
* Crea una sala de chat a través de la interfaz de administración de Django (localhost:8080/admin/)
* "twistd -y chatserver.py", aunque probablemente "twistd -n -y chatserver.py" sea más apropiado ya que es poco probable que vayas a usar esto en producción en algún momento

Para ver el servicio de chat en acción: 
* una lista de salas de chat existentes está en localhost:8000/chats
* chatea por WebSockets en localhost:8000/chats/[room_id]
* chatea por HTTP, con un servicio de long-polling, en localhost:8000/chats/long_poll/[room_id]

**DEPENDENCIAS**

Ten en cuenta que me baso en la rama websockets (usé [websocket-4173-4](https://github.com/twisted/twisted/tree/websocket-4173-4)) de Twisted, así que asegúrate de instalarla (creo que aún no se ha fusionado en la rama principal)   

Consulta requirements.txt para las versiones de las dependencias. 

He estado ejecutando todo en un virtualenv estándar de python2.7, con pip para la gestión de paquetes

**POR HACER:**
 * Integrar la autenticación de Twisted y Django
 * hacer que Twisted registre los chats en la base de datos de Django
 * una interfaz de usuario agradable para crear salas de chat, etc....
