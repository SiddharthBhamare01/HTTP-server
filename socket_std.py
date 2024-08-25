import socket
import config as cfg
class serverSocket:
	def __init__(self, host, port):
		
		self.host = host
		self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.timeout=cfg.time_out
		self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.serversocket.bind((host, port))
		self.serversocket.setblocking(False)
		self.serversocket.listen(cfg.max_listen)
		self.port = self.serversocket.getsockname()[1]

	def accept(self):
		clientConnection, clientAddress = self.serversocket.accept()
		clientConnection.settimeout(self.timeout)
		return clientConnection,clientAddress

	def receive(self, clientConnection, bufSize):
		return clientConnection.recv(bufSize)

	def send(self, clientConnection, response):
		clientConnection.sendall(response)
	
	def close(self, clientConnection):
		clientConnection.close()