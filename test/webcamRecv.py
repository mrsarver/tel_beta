import socket
from PIL import Image


TCP_IP = '127.0.0.1'
TCP_PORT = 5007
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()

print 'Connection address:', addr
message = ""
while 1:
	data = conn.recv(BUFFER_SIZE)
	if not data: break
	message = message + data

messageLength = len(message)

if messageLength:
	im = Image.fromstring('RGB', (640, 480), message)
	im.save("test.png")

conn.close()