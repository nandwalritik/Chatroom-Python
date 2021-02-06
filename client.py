import socket
import threading

class Client:
	
	def __init__(self):
		self.create_connection()

	def create_connection(self):
		self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

		while True:
			try:
				host = input("Enter host :- ")
				port = int(input('Enter port :- '))
				self.client.connect((host,port))
				break
			except:
				print("Error in connecting to server")

		self.username = input('Enter username --> ')
		self.client.send(self.username.encode())

		message_handler = threading.Thread(target=self.handle_messages,args=())
		message_handler.start()

		input_handler = threading.Thread(target=self.input_handler,args=())
		input_handler.start()

	def handle_messages(self):
		while True:
			print(self.client.recv(2048).decode())

	def input_handler(self):
		while True:
			self.client.send((self.username+' - '+input()).encode())
client=Client()