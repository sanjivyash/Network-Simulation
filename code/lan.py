class LAN:
	def __init__(self, name):
		self.name = name
		self.connections = set()
		self.hosts = set()

	def connect(self, bridge):
		self.connections.add(bridge) 

	def network(self, host):
		self.hosts.add(host)

	def forward(self, message, t):
		sender = message[2]

		for bridge in self.connections:
			if bridge is not sender:
				bridge.receive(message, self, t)

	def transmit(self, sender, header, t):
		origin, destination = header

		for bridge in self.connections:
			if bridge is not sender:
				port = bridge.transmit(self, header, t+1)

	def __repr__(self):
		return self.name