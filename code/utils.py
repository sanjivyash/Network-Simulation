class Bridge:
	def __init__(self, name, idx, flag):
		self.name = name
		self.id = idx

		self.connections = set()
		self.root = self
		self.dist = 0
		
		self.rp = None
		self.next = None 

		self.forward = False
		self.table = {}

		self.flag = flag
		self.trace = []

	def connect(self, lan):
		self.connections.add(lan)

	def send(self, t):
		if self.root is self or self.forward:
			if self.flag:
				self.trace.append(f'{t} s {self} ({self.root} {self.dist} {self})')
			
			for lan in self.connections:
				lan.receive((self.root, self.dist, self), t)
			
			self.forward = False

	def receive(self, msg, lan, t):
		root, dist, bridge = msg

		if self.flag:
			self.trace.append(f'{t+1} r {self} ({root} {dist} {bridge})')
		
		dist += 1

		if root.id > self.root.id or (root.id == self.root.id and dist > self.dist):
			return
		if self.next:
			if root.id == self.root.id and dist == self.dist and bridge.id > self.next.id:
				return 

		self.forward = True
		self.root = root
		self.dist = dist 
		self.rp = lan
		self.next = bridge

	def active(self, lan):
		return self.rp is lan or lan.dp is self

	def transmit(self, sender, header, t):
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


class LAN:
	def __init__(self, name):
		self.name = name
		self.connections = set()
		self.hosts = set()
		self.dp = None
		self.root = None
		self.dist = None
		self.buffer = []

	def connect(self, bridge):
		self.connections.add(bridge) 

	def network(self, host):
		self.hosts.add(host)

	def send(self):
		while self.buffer:
			message, t = self.buffer.pop()
			sender = message[2]

			for bridge in self.connections:
				if bridge is not sender:
					bridge.receive(message, self, t)

	def receive(self, message, t):
		self.buffer.append((message, t))
		root, dist, sender = message

		if self.root is None:
			self.root = root
			self.dist = dist
			self.dp = sender
			return

		if root.id > self.root.id or (root.id == self.root.id and dist > self.dist):
			return
		if root.id == self.root.id and dist == self.dist and sender.id > self.dp.id:
			return 

		self.root = root 
		self.dist = dist
		self.dp = sender

	def active(self, bridge):
		return self.dp is bridge or bridge.rp is self

	def transmit(self, sender, header, t):
		origin, destination = header

		for bridge in self.connections:
			if self.active(bridge) and bridge is not sender:
				port = bridge.transmit(self, header, t+1)

	def __repr__(self):
		return self.name