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
