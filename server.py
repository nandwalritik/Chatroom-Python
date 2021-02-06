import socket
import threading

class Server:
	def __init__(self):
		self.start_server()

	def start_server(self):
		self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

		host = socket.gethostbyname(socket.gethostname())
		port = int(input('Enter port :- '))

		self.clients = []

		self.server.bind((host,port))
		self.server.listen(100)

		print('Server Host :- '+str(host))
		print('Server Port :- '+str(port))

		self.username_lookup = {}

		while True:
			conn,addr = self.server.accept()

			username = conn.recv(2048).decode()

			print(str(username)+' Joined')
			self.broadcast(username)
			self.username_lookup[conn] = username
			self.clients.append(conn)

			threading.Thread(target=self.handle_client,args=(conn,addr,)).start()

	def broadcast(self,message):
		for connection in self.clients:
			connection.send(message.encode())

	def handle_client(self,conn,addr):
		while True:
			try:
				message = conn.recv(2048)
			except:
				conn.shutdown(socket.SHUT_RDWR)
				self.clients.remove(conn)

				print(str(self.username_lookup[conn])+"left the group")
				break
			if message.decode() != '':
				print(str(message.decode()))
				for connection in self.clients:
					if connection != conn :
						connection.send(message)

server = Server()
