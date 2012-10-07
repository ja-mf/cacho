import logging

from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin
from socketio.sdjango import namespace

from cacho_app.models import GameUser, GameRoom

from django.http import HttpResponse
from dudo import DudoGame

# este modulo maneja la interaccion de gevent-socketio (parte del servidor)
# con el javascript del cliente (socket.io). estan definidos metodos de un namespace
# (ver documentacion de gevent-socketio), las cuales se ejecutaran dependiendo del mensaje 
# para cada peticion, es una instancia de este namespace, se puede acceder al
# request object naturalmente, como self.request y asi obtener variables de session y
# de otro interes
@namespace('/game')
class GameNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):
	 
	capacidad = 3

	def initialize(self): 
		self.logger = logging.getLogger("socketio.chat")
		self.log("Socketio session started")

		  # entro un usuario, unirlo a la sala:
		  #self.room = room
		  # prueba de acceso al request object en el namespace.
		  # faltaria hacer un modelo de datos para cada room,
		# hacer la instancia de la logica de juego, un controlador para room si es que se quiere
		  
		self.username = self.request.user.username
		self.emit('session_data', self.username)
		self.log('Usuario: {0}'.format(self.username))
		self.broadcast_event('announcement', '%s has connected' % self.username)

	def log(self, message):
		self.logger.info("[{0}] {1}".format(self.socket.sessid, message))
 
	def on_join(self, room_in):
		self.usuarios_room = GameUser.objects.filter(room=room_in)
		if (self.usuarios_room.count() < self.capacidad):
			
			self.room = room_in
			self.join(room_in)
			user = GameUser(user=self.request.user, room=GameRoom.objects.get(pk=self.room), session=self.socket.sessid)
			user.save()

			# ahora usuarios_room es una lista de usuarios en la sala (strings)
			# esto es hecho gracias a values_list, de otra forma, serian objetos.
			self.usuarios_room = list(GameUser.objects.values_list('user__username', flat=True).filter(room=room_in))
	
			# emitir la lista de usuarios al cuarto y al usuario conectado
			self.emit_to_room(self.room, 'usuarios_room', self.usuarios_room)
			self.emit('usuarios_room', self.usuarios_room)
		else:
			self.emit('server_message', 'ta llenoe')

#		self.log(self.room)
		return True
 
	def recv_disconnect(self):
		# borrar usuario de la db
		# emitir nueva lista de usuarios
		self.log('Desconectado')
		self.broadcast_event('announcement', '%s has disconnected' % self.username)
		d = GameUser.objects.get(session=self.socket.sessid)
		d.delete()
		self.log('user %s deleted from db.' % self.username)

		self.usuarios_room = list(GameUser.objects.values_list('user__username', flat=True).filter(room=self.room))

		self.emit_to_room(self.room, 'usuarios_room', self.usuarios_room)
		self.disconnect(silent=True)
		return True
	
	def on_user_message(self, msg):
		self.log('User message: {0}'.format(msg))
		self.emit_to_room(self.room, 'msg_to_room',
		 	self.username, msg)
		return True