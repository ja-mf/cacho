import logging

from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin
from socketio.sdjango import namespace

from django.http import HttpResponse


# este modulo maneja la interaccion de gevent-socketio (parte del servidor)
# con el javascript del cliente HTML5. estan definidos metodos de un namespace
# (ver documentacion de gevent-socketio), las cuales se ejecutaran dependiendo del mensaje 

@namespace('/chat')
class ChatNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):
	 nicknames = []

	 def initialize(self):
		  self.logger = logging.getLogger("socketio.chat")
		  self.log("Socketio session started")

		  # entro un usuario, unirlo a la sala:
		  #self.room = room
		  # prueba de acceso al request object en el namespace.
		  # faltaria hacer un modelo de datos para cada room,
# hacer la instancia de la logica de juego, un controlador para room si es que se quiere
		  
		  user_name = self.request.user.get_full_name()
		  self.emit('session_data', user_name)
		  self.log('Nickname: {0}'.format(user_name))
		  self.nicknames.append(user_name)
		  self.socket.session['nickname'] = user_name
		  self.broadcast_event('announcement', '%s has connected' % user_name)
		  self.broadcast_event('nicknames', self.nicknames)
  #		return True, nickname

	 def log(self, message):
		  self.logger.info("[{0}] {1}".format(self.socket.sessid, message))
	 
	 def on_join(self, room):
		  self.room = room
		  self.join(room)
		  self.log(room)
		  return True
		  
	 def on_nickname(self, nickname):
		  self.log('Nickname: {0}'.format(nickname))
		  self.nicknames.append(nickname)
		  self.socket.session['nickname'] = nickname
		  self.broadcast_event('announcement', '%s has connected' % nickname)
		  self.broadcast_event('nicknames', self.nicknames)
		  return True, nickname

	 def recv_disconnect(self):
		  # Remove nickname from the list.
		  self.log('Disconnected')
		  nickname = self.socket.session['nickname']
		  self.nicknames.remove(nickname)
		  self.broadcast_event('announcement', '%s has disconnected' % nickname)
		  self.broadcast_event('nicknames', self.nicknames)
		  self.disconnect(silent=True)
		  return True

	 def on_user_message(self, msg):
		  self.log('User message: {0}'.format(msg))
		  self.emit_to_room(self.room, 'msg_to_room',
				self.socket.session['nickname'], msg)
		  return True
