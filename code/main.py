from utils import Bridge, LAN


def parse(inp):
	vals = inp.split()
	return vals[0][:-1], vals[1:]


def spanningTree(bridges, lans, flag):
	run  = True
	t = 1

	while run:
		# send or forward config messages from bridges
		for i in bridges:
			bridges[i].send(t)
		t += 1

		# check if some bridge was mutated
		run = False

		for i in bridges:
			if bridges[i].mutate:
				run = True
				break

	# print trace output
	if flag:
		trace = []
		
		for i in bridges:
			trace.extend(bridges[i].trace)
			bridges[i].trace.clear()
		print('\n'.join(sorted(trace)))

	# print required output
	for i in bridges:
		bridge = bridges[i]
		output = []

		for lan in bridge.connections:
			if bridge.rp is lan:
				output.append(f'{lan}-RP')
			elif lan in bridge.dp:
				output.append(f'{lan}-DP')
			else:
				output.append(f'{lan}-NP')

		print(f'{bridge}: ' + ' '.join(sorted(output)))


def pathways(bridges, lans, tasks, flag):
	hosts ={}

	for i in lans:
		for h in lans[i].hosts:
			hosts[h] = lans[i]

	for task in tasks:
		origin, destination = task
		hosts[origin].transmit(None, task, 0)

		# print trace output
		if flag:
			trace = []
			
			for i in bridges:
				trace.extend(bridges[i].trace)
				bridges[i].trace.clear()
			print('\n'.join(sorted(trace)))

		# print required output
		for i in range(len(bridges)):
			print(f'{bridges[i]}:')
			print('HOST ID | FORWARDING PORT')

			output = []
			for host, port in bridges[i].table.items():
				output.append(f'{host} | {port}')
			print('\n'.join(sorted(output)))

		print()


if __name__ == '__main__':
	flag = (input() == '1')
	B = int(input())
	bridges = {}
	lans = {}

	for i in range(B): 
		bridge, ports = parse(input())
		bridges[i] = Bridge(bridge, i, flag) 

		for p in ports:
			if p not in lans:
				lans[p] = LAN(p)

			bridges[i].connect(lans[p])
			lans[p].connect(bridges[i])

	for i in range(len(lans)):
		p, host = parse(input())

		for h in host:
			lans[p].network(h)

	L = int(input())
	tasks = []

	for i in range(L):
		tasks.append(input().split())

	spanningTree(bridges, lans, flag)
	pathways(bridges, lans, tasks, flag)