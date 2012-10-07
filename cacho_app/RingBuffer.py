class RingBuffer:
	def __init__(self):
		self.data = []
		self.cur=0
	def append(self,x):
		"""append an element at the end of the buffer"""
		self.data.append(x)
	def get(self):
		self.cur+=1
		if len(self.data) == self.cur:
			self.cur=0 	
		return self.data[self.cur]

class Dudo:
	def posibles(self, movimiento, maximo_dados):
		movimientos_posibles = []
		pinta = 0
		for i in range (movimiento[0]+1, maximo_dados+1):
			if ((movimiento[1] != 1) and (pinta == 0)):
				for j in range (movimiento[1]+1, 7):
					movimientos_posibles.append((i,j))
				pinta = 1
			else:
				for j in range (1,7):
					movimientos_posibles.append((i,j))
		return movimientos_posibles
