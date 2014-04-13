from PIL import Image, ImageTk
import cv2
import socket

TCP_PORT = 5007
TCP_IP = "127.0.0.1"

cap = cv2.VideoCapture(0)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((TCP_IP, TCP_PORT))


ret, img = cap.read()
img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
img = Image.fromarray(img)
print img.size
img_str = img.tostring()


sock.sendall(img_str)
sock.close()

cap.release()