from Tkinter import *
from PIL import Image, ImageTk
from threading import *
import tkMessageBox
import re
import cv2

class Application(Frame):
	def createWidgets(self):
		"""Construct Graphical User Interface Buttons"""
		self.IPLABEL = Label(self, text = "Src IPv4 Address:")

		self.IPENTRY = Entry(self, width=15)
		self.IPENTRY.focus_set()

		self.NEW = Button(self, text="New Call to IP", command=self.newCall)
		self.END = Button(self, text="End Call", command=self.endCall)
		self.QUIT = Button(self, text="Quit", command=self.exit)
		self.FRAME = Label(self, image=self.picture)

		self.IPLABEL.grid(row=0, column=0, sticky=W)
		self.IPENTRY.grid(row=0, column=1, columnspan=2)
		self.NEW.grid(row=1, column=0, sticky=W+E)
		self.END.grid(row=1, column=1, sticky=W+E)
		self.QUIT.grid(row=1, column=2, sticky=W+E)
		self.FRAME.grid(row=2, column=0, columnspan=3)

		self.appMenu = Menu(self)
		self.fileMenu = Menu(self.appMenu, tearoff=0)
		self.fileMenu.add_command(label="New Call", command=self.newCall)
		self.fileMenu.add_command(label="End Call", command=self.endCall)
		self.fileMenu.add_separator()
		self.fileMenu.add_command(label="Exit", command=self.exit)
		self.appMenu.add_cascade(label="File", menu=self.fileMenu)

	def newCall(self):
		"""Initialize a new call to a specified IP"""
		ip = self.IPENTRY.get()

		if self.isValidIP(ip) == None or ip == "0.0.0.0":
			tkMessageBox.showerror("Invalid IPv4 address", ip + "is an invalid IPv4 address.  Please enter a valid IPv4 address.")
			self.IPENTRY.focus_set()
			self.IPLABEL["fg"] = "red"
			self.FRAME["image"] = self.derp
			return False

		self.IPLABEL["fg"] = "black"

		if self.VideoThread == None:
			self.VideoThread = Thread(target = self.webcamCap)
			self.VideoThread.daemon = True
			self.callActive = True
			self.VideoThread.start()
			return True
		else:
			tkMessageBox.showerror("End Current Call",  "Please end the current call before making a new one")
			return False

	def endCall(self):
		"""End the current call"""
		if self.VideoThread == None:
			tkMessageBox.showerror("No Current Call",  "No current call to end")
			return False

		self.callActive = False
		self.VideoThread.join()
		self.VideoThread = None
		self.FRAME["image"] = self.picture

	def exit(self):
		"""Proper exiting and resource management"""
		if tkMessageBox.askyesno("Quit?", "Are you sure you want to exit?  This will end any calls you are making."):
			self.endCall()
			self.quit()

	def isValidIP(self, ip):
		"""Returns None if invalid, match object otherwise"""
		#the magic begins here
		p = re.compile('^(([1-9]?\d|1\d\d|25[0-5]|2[0-4]\d)\.){3}([1-9]?\d|1\d\d|25[0-5]|2[0-4]\d)$')
		return p.match(ip)

	def webcamCap(self):
		self.cap = cv2.VideoCapture(0)
		#i feel ashamed of this loop
		while self.callActive:
			self.ret, self.img = self.cap.read()
			self.img = cv2.cvtColor(self.img,cv2.COLOR_BGR2RGB)
			#if self.rotate == True:
				#self.img.transpose(Image.FLIP_LEFT_RIGHT)
			self.img = ImageTk.PhotoImage(image = Image.fromarray(self.img))
			self.FRAME["image"] = self.img
			self.FRAME._image_cache = self.img
		self.cap.release()


	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.picture = ImageTk.PhotoImage(Image.open("telsmall.png"))
		self.derp = ImageTk.PhotoImage(Image.open("derp.jpg"))
		self.createWidgets()
		self.VideoThread = None
		self.callActive = False
		self.rotate = True
		self.grid()

if __name__ == "__main__":
	app = Application()
	app.master.title("Tel v 0.0.1")
	#app.master.maxsize(512, 512)
	app.master.config(menu=app.appMenu)
	app.master.protocol("WM_DELETE_WINDOW", app.exit)
	app.mainloop()