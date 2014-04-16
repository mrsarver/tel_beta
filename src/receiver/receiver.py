import threading
import socket
import Queue

class Receiver(threading.Thread):
	"""A wrapper for threading.Thread that is the receiving end of the project"""

	def run(self):
		"""The actual server part of the code"""
		self.isRunning = True

		while self.isRunning:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.bind((self.ip, self.port))
			self.sock.listen(1)
			conn, addr = self.sock.accept()
			#print "connected!"
			message = ""
			while True:
				data = conn.recv(self.buffer)
				if not data:break
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
		self.isRunning = False
		threading.Thread.__init__(self)

if __name__ == "__main__":
	myQueue = Queue.Queue()
	myThread = Receiver(5007, myQueue)
	myThread.start()
	