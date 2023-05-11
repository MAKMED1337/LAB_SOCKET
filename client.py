import socket
from config import *
from connection import Connection
import logging

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%H:%M:%S',
			filename='client.log', filemode='w', level=logging.INFO)

numbers = set([int(i) for i in input('Enter client numbers: ').split(' ')])
s = set([])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
	sock.connect((HOST, PORT))
	conn = Connection(sock)
	conn.send('who')
	print(conn.recv())
	
	for i in numbers:
		conn.send(PREFIX + str(i))

		res = conn.recv()
		assert res in ('OK', 'BAD')

		print(i, '->', res)
		if res == 'OK':
			s.add(i)
	
	conn.send('reverse')
	assert conn.recv() == 'reverse'

	while True:
		i = conn.recv()

		if i == 'end':
			break

		s.add(int(i))
		print('server ->', i)
print(s)