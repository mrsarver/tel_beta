from PIL import Image, ImageTk
import socket

TCP_PORT = 5007
TCP_IP = "127.0.0.1"

img = Image.open("telsmall.png")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((TCP_IP, TCP_PORT))

print img.size
img_str = img.tostring()
sock.sendall(img_str)
sock.close()