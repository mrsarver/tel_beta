import threading
import socket
import Queue
from PIL import Image, ImageTk
import cv2

class Sender(threading.Thread):
	def run(self):
		"""Gets a object from the shared Queue and sends it"""
		while self.isRunning:
			if not self.q.empty():
				self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				self.sock.connect((self.dest_ip, self.dest_port))
				message = self.q.get()
				self.sock.sendall(message)
				#send break frame message - consider an empty sendall
				self.sock.close()

	def __init__(self, ip, port, q):
		self.dest_ip = ip
		self.dest_port = port
		self.q = q
		self.isRunning = True
		threading.Thread.__init__(self)

if __name__ == "__main__":
	myQueue = Queue.Queue()
	myThread = Sender('127.0.0.1', 5007, myQueue)
	myThread.start()
	cap = cv2.VideoCapture(0)
	ret, img = cap.read()
	img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
	img = Image.fromarray(img)
	message = img.tostring()
	myQueue.put(message)
	cap.release()
	