import socket
from connection import Connection
from config import *
import logging

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%H:%M:%S',
			filename='server.log', filemode='w', level=logging.INFO)

MAX_NUMBER = 1337

numbers = set([int(i) for i in input('Enter server numbers: ').split(' ')])

def process_connection(conn: Connection):
	s = set()
	def process_command(command: str) -> str:
		nonlocal s
		if command == 'who':
			return 'Tikhoniuk Eduard #30\nNumber set synchroniztion'
		if command == 'reverse':
			return 'reverse'
		
		if not command.startswith(PREFIX):
			return 'wrong command'
	
		try:
			num = int(command[len(PREFIX):])
		except Exception:
			return 'wrong command'
		
		if num > MAX_NUMBER:
			return 'BAD'
		else:
			s.add(num)
			return 'OK'

	receiving = True
	while receiving:
		for command in conn.recv_commands():
			if command == 'reverse':
				receiving = False
			conn.send(process_command(command))

	for i in numbers - s:
		conn.send(str(i))
	conn.send('end')

	s.update(numbers)
	return s

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind((HOST, PORT))
	s.listen()

	while True:
		sock, addr = s.accept()
		with sock:
			print(addr, '->', process_connection(Connection(sock)))