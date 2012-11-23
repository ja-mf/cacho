import logging

from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin
from socketio.sdjango import namespace

from cacho_app.models import GameUser, GameRoom

from django.http import HttpResponse
from Dudo import Dudo, RingBuffer

import redisutils
import json
import random

# este modulo maneja la interaccion de gevent-socketio (parte del servidor)
# con el javascript del cliente (socket.io). estan definidos metodos de un namespace
# (ver documentacion de gevent-socketio), las cuales se ejecutaran dependiendo del mensaje 
# para cada peticion, es una instancia de este namespace, se puede acceder al
# request object naturalmente, como self.request y asi obtener variables de session y
# de otro interes
@namespace('/game')
class GameNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):
	 
	capacidad = 3
	turnos = {}
	dados = {}
	el_dudo = Dudo()
#	redisdb = redis.StrictRedis(host='localhost', port=6379, db=0)
	totaldados = {}
	actualdados = {}
	firstplay = {}
	current_play = {}

	def initialize(self): 
		self.logger = logging.getLogger("socketio.chat")
		self.log("socket.io session started!")
		self.username = self.request.user.username
		self.emit('session_data', self.username)
		self.log('Usuario: {0}'.format(self.username))
		self.broadcast_event('announcement', '%s se ha conectado' % self.username)

	def log(self, message):
		self.logger.info("[{0}] {1}".format(self.socket.sessid, message))

	# entrar a la sala
	def on_join(self, room_in):
		# cantidad de usuarios en la sala actual
		u = redisutils.get_members(room_in)

		if (u < self.capacidad):
			# si la sala esta vacia, crear el RingBuffer para manipular los turnos
			# el indice del diccionario "turnos" sera el room id
			if (u == 0):
				self.turnos[room_in] = RingBuffer()
			
			self.turnos[room_in].append(self.socket.sessid)
			self.log(self.turnos[room_in].data)

			# variables de instancia, join agregara el usuario al room manejado por el socket
			# agregar al usuario a la db
			self.room = room_in
			self.join(room_in)
			
			# new, redis (session)
			# user_sessid = {'user_id': userid, 'user_name': username, 'dados': [0,0,0,0,0], 'confirm': 0}
			# room_roomname = ['sessid1', 'sessid2', ...]
			# bajo este concepto, para formatear la lista de usuarios con las confirmaciones y dados
			# para enviarselos a los clientes en una sala, se referira primero al room_roomname, para luego referirse al key
			# user_sessid de todos los ususarios en la sala.
			user_session = json.dumps({'user_id': self.request.user.id, 
												'user_name': self.request.user.username,
												'confirm': False})

			dados_session = json.dumps({'dados': [0]*5})

			redisutils.redisdb.set('user_' + self.socket.sessid, user_session)
			redisutils.redisdb.set('dados_' + self.socket.sessid, dados_session)
			redisutils.redisdb.sadd('room_' + self.room, self.socket.sessid)
			self.log(user_session)

			self.emit('user_sessid', self.socket.sessid)

			# devolver la nueva lista de usuarios con las confirmaciones
			self.emit_to_room(self.room, 'usuarios_room', redisutils.get_members_info(self.room))
			self.emit('usuarios_room', redisutils.get_members_info(self.room))

		else:
			self.emit('server_message', 'ta llena la sala oe')

		return True
 
	def recv_disconnect(self):
		# se ha desconectado un usuario:
		# - borrar usuario de la db
		# - sacarlo del RingBuffer
		# - emitir nueva lista de usuarios
		self.log('Desconectado')
		self.broadcast_event('announcement', '%s se ha desconectado' % self.username)

		redisutils.redisdb.srem('room_' + self.room, self.socket.sessid)
		redisutils.redisdb.delete('user_' + self.socket.sessid)
		redisutils.redisdb.delete('dados_' + self.socket.sessid)

		# falta sacarlo del ringbuffer aqui

		self.emit_to_room(self.room, 'usuarios_room', redisutils.get_members_info(self.room))

		self.disconnect(silent=True)

		return True
	
	def on_confirmar(self, action):
		# se ha recibido una confirmacion
		# invertir la confirmacion actual
		
		u = json.loads(redisutils.redisdb.get('user_' + self.socket.sessid))
		u['confirm'] = not(u['confirm'])
		redisutils.redisdb.set('user_' + self.socket.sessid, json.dumps(u))
		self.totaldados[self.room] = 0
		self.actualdados[self.room] = 0

		# emitir nueva lista de usuarios y confirmaciones
		users = redisutils.get_members_info(self.room)
		self.emit_to_room(self.room, 'usuarios_room', users)
		self.emit('usuarios_room', users)

		# verificar que todos hayan confirmado
		for c in users:
			if c['confirm'] == False:
				return True

		self.emit_to_room(self.room, 'server_message', 'todos_confirmaron')
		self.emit('server_message', 'todos_confirmaron')

		# tirar dados, turno y jugadas posibles
		for sessid in redisutils.redisdb.smembers('room_' + self.room):
			dados = [random.randint(1,6) for i in range(5)]
			redisutils.redisdb.set('dados_' + sessid, json.dumps(dados))
			self.totaldados[self.room] += 5
			self.actualdados[self.room] += 5

#		users =  redisutils.get_members_info(self.room)
#		self.emit_to_room(self.room, 'usuarios_room', users)
#		self.emit('usuarios_room', users)

		self.firstplay[self.room] = 1
		turno = self.turnos[self.room].get()
		self.emit_to_room(self.room, 'turno', turno)
		self.emit('turno', turno)

	# enviar dados al usuario que los pidio
	def on_get_dados(self):
		# tirar dados?
		self.emit('dados', redisutils.redisdb.get('dados_' + self.socket.sessid))
		return True
		
	# enviar jugadas posibles al usuario que las pidio, n es el numero de dados
	def on_get_jugadas_posibles(self):
		n = self.actualdados[self.room]
		
		if (self.firstplay[self.room]):
			self.emit('jugadas_posibles', self.el_dudo.posibles((0, 6), n))
			self.firstplay[self.room] = 0
		else: 
			self.emit('jugadas_posibles', self.el_dudo.posibles(self.current_play[self.room], n))
		

	def on_jugada(self, j):
		# se recibio una jugada:
		# pasar turno, si jugada es dudo o calzo, revisar y actualizar la lista de dados del usuario y tirar dados para todos.
		# comprobar si alguien gano
		# GAME LOOP
		# jugada[0] = numero de dados
		# jugada[1] = pinta
		# comprobar que la jugada es valida
		# (0, 0) indica calzo
		# (0, 1) indica dudo
		jugada = (j[0], j[1])
		
		# movimientos para quitar o ganar un dado
		usuarios = redisutils.redisdb.smembers(self.room)

		# dados_mesa, el total de dados que hay en la mesa
		dados_mesa = []
		for u in usuarios:
			dados_mesa.append(json.loads(redisutils.redisdb.get('dados_' + u)))
		
		# flatten list!
		dados_mesa = [item for sublist in dados_mesa for item in sublist]
		
		if jugada[1] != 1:
			# aces + pinta
			nreal = dados_mesa.count(1) + dados_mesa.count(jugada[1])
		else:
			nreal = dados_mesa_count(1)

		n = redisutils.redisdb.get('dados_' + self.socket.sessid)

		# es calzo
		if jugada == (0,0):
			if (jugada[0] == nreal):
				n.append('0')
			else:
				n.pop()

			redisutils.redisdb.set('dados_' + self.socket.sessid, n)

		# es dudo
		elif jugada == (0,1):
			if (jugada[0] < nreal):
				pass
				# weas pa quitarle un dado al anterior
			
		# enviar turno
		turno = self.turnos[self.room].get()
		self.emit_to_room(self.room, 'turno', turno)
		self.emit('turno', turno)

	def on_user_message(self, msg):
		self.log('mensaje: {0}'.format(msg))
		self.emit_to_room(self.room, 'msg_to_room',
		 	self.username, msg)
		return True
