import threading
import socket
import Queue

class Server(threading.Thread):
	"""A wrapper for threading.Thread that is the receiving end of the project"""

	def run(self):
		"""The actual server part of the code"""
		self.sock.listen(1)
		conn, addr = self.sock.accept()
		message = ""
		while True:
			data = conn.recv(self.buffer)
			if not data: break
			message = message + data

		message_len = len(message)

		if message_len:
			self.q.put(message)
		conn.close()

	def __init__(self, port, q):
		"""Initiate the queue and get the port"""
		self.ip = '127.0.0.1'
		self.port = port
		self.q = q
		self.buffer = 1024
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind((self.ip, self.port))
		threading.Thread.__init__(self)

if __name__ == "__main__":
	myQueue = Queue.Queue()
	myThread = Server(5007, myQueue)
	myThread.start()