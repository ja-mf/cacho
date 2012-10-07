import random

class Player:
	"""
	Clase que contendra los metodos y variables de un
	jugador especifico
	"""
	dados = []
	def __init__(self, n):
		for i in range	(6):
			self.dados[i] = random.randint(1,6)
	

class DudoGame:
	"""
	Clase que implementa una instancia del juego.
	Pertenece a una partida de dudo.
	"""
	# TODO: 
	# - establecer formato para la lista de jugadas (movements)
	# - codear nextMovements(self), metodo que tomara los movimientos hechos
	# guardados en movements y calculara los movimientos posibles.

	# lista de jugadores y jugadas
	players = []
	movements = []

	# inicio del juego, primer turno aleatorio
	# establecer numero de dados en la mesa.
	# construir Player para cada jugador y agregarlo a players[]
	def __init__(self):
		
		# agregar los jugadores al juego
		#for p in self.players:
		#	self.players.append(p)

		# elegir a un jugador para el inicio del turno
		#self.turn = random.choice(self.players)
		pass
	# implementar logica del juego para calcular
	# las proximas jugadas para el turno actual, dependiendo de 
	# "movements" (stack de jugadas anteriores)
	# debe retornar una lista con tales jugadas.
	def nextMovements(self):
		pass

		
