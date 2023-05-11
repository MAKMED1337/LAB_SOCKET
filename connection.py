import socket
import logging

logger = logging.getLogger('connection')

class Connection:
	sock: socket.socket

	def __init__(self, sock: socket.socket):
		self.sock = sock

	def send_commands(self, commands: list[str]):
		for command in commands:
			assert ';' not in command, 'commands must not contain \''
		self.send(';'.join(commands))

	def send(self, data: str):
		assert len(data) < 255, 'cannot send, too many data'
		logger.info('sedning: %s', data)
		self.sock.sendall((len(data) + 1).to_bytes() + data.encode('ascii'))
	
	def _recv_exactly(self, length) -> bytearray:
		buf = bytearray(length)
		view = memoryview(buf)
		while length > 0:
			nbytes = self.sock.recv_into(view, length)
			view = view[nbytes:]
			length -= nbytes
		return buf

	def recv(self) -> str:
		length = int.from_bytes(self._recv_exactly(1)) - 1
		data = self._recv_exactly(length).decode('ascii')
		logger.info('received: %s', data)
		return data
	
	def recv_commands(self) -> list[str]:
		return self.recv().split(';')