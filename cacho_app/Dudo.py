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
	def get_current(self):
		return self.data[self.cur]
	def previous(self):
		self.cur-=1
		if self.cur < 0:
			self.cur = len(self.data)-1
		return self.data[self.cur]
	def set(self, x):
		self.cur=x



class Dudo:
	def posibles(self, movimiento, maximo_dados):
		movimientos_posibles = []
		pinta = 0
		if movimiento[1] != 1:
			for i in range (movimiento[0], maximo_dados+1):
				if pinta == 0:
					if movimiento[0]!=0:
						movimientos_posibles.append(((movimiento[0]/2)+1,1))
					for j in range (movimiento[1]+1, 7):
						movimientos_posibles.append((i,j))
					pinta = 1
				else:
					for j in range (1,7):
						movimientos_posibles.append((i,j))
		else:
			for i in range (movimiento[0]+1, maximo_dados+1):
				movimientos_posibles.append((i,1))
			for i in range (movimiento[0]*2, maximo_dados+1):
				for j in range (2, 7):
					movimientos_posibles.append((i,j))
		return movimientos_posibles
