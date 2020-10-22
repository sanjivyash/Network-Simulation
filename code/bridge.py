class Bridge:
	def __init__(self, name, idx, flag):
		self.name = name
		self.id = idx

		self.connections = set()
		self.root = self
		self.dist = 0
		
		self.rp = None
		self.dp = set()
		self.next = None 

		self.mutate = False
		self.forward = False
		self.table = {}

		self.flag = flag
		self.trace = []

	def connect(self, lan):
		self.connections.add(lan)
		self.dp.add(lan)

	def send(self, t):
		if self.root is self or self.forward:
			if self.flag:
				self.trace.append(f'{t} s {self} ({self.root} {self.dist} {self})')
			
			for lan in self.connections:
				lan.forward((self.root, self.dist, self), t)
			
		self.mutate = False
		self.forward = False

	def receive(self, msg, lan, t):
		root, dist, bridge = msg
		
		if self.flag:
			self.trace.append(f'{t+1} r {self} ({root} {dist} {bridge})')

		if self.dist > dist or (self.dist == dist and self.id > bridge.id): 
			if lan in self.dp:
				self.dp.remove(lan)
				self.mutate = True
		
		dist += 1

		if root.id > self.root.id or (root.id == self.root.id and dist > self.dist):
			return
		if self.next:
			if root.id == self.root.id and dist == self.dist and bridge.id > self.next.id:
				return

		self.mutate = True
		self.forward = True
		self.root = root
		self.dist = dist
		self.rp = lan
		self.next = bridge

	def active(self, lan):
		return self.rp is lan or lan in self.dp

	def transmit(self, sender, header, t):
		if not self.active(sender):
			return

		origin, destination = header
		self.table[origin] = sender

		if self.flag:
			self.trace.append(f'{t} r {self} {origin}-->{destination}')
			self.trace.append(f'{t} s {self} {origin}-->{destination}')

		if destination in self.table:
			if self.table[destination] is not sender:
				self.table[destination].transmit(self, header, t)
			return

		for lan in self.connections:
			if self.active(lan) and lan is not sender:
				lan.transmit(self, header, t)
		
	def __repr__(self):
		return self.name 