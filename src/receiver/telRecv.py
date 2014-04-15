from Tkinter import *
from PIL import Image, ImageTk
import tkMessageBox
import Queue
import server

class Application(Frame):
	def createWidgets(self):
		"""Construct Graphical User Interface"""
		#default skype port is 23399
		self.serverPort = IntVar()
		self.PORTLABEL = Label(self, text="LISTEN ON PORT: ")
		self.PORTENTRY = Entry(self, width=5, textvar=self.serverPort)
		self.BUTNSTART = Button(self, text="Start listening", command=self.startServer)
		self.PICTFRAME = Label(self, image=self.picture)

		self.PORTLABEL.grid(row=0, column=0)
		self.PORTENTRY.grid(row=0, column=1)
		self.BUTNSTART.grid(row=0, column=2)
		self.PICTFRAME.grid(row=1, column=0, columnspan=3)

		self.PORTENTRY.focus_set()
		pass

	def loadPictures(self):
		"""Loads the initial tel image"""
		self.picture = ImageTk.PhotoImage(Image.open("../telsmall.png"))

	def loadQueue(self):
		"""Initialize a queue for image storage"""
		self.frameQueue = Queue.Queue()

	def startServer(self):
		"""Initiate the server"""
		self.flag = True
		self.serverPort = self.PORTENTRY.get()
		self.serverPort = int(self.serverPort)
		if self.serverPort > 1024:
			self.serverThread = server.Server(self.serverPort, self.frameQueue)
			self.serverThread.start()
			while self.flag:
				if not self.frameQueue.empty():
					self.flag = False
					message = self.frameQueue.get()
					print "got message"
					im = Image.fromstring('RGB', (640, 480), message)
					im = ImageTk.PhotoImage(image = im)
					self.PICTFRAME["image"] = im
					self.PICTFRAME._image_cache = im
				else:
					continue
		else:
			tkMessageBox.showerror("Invalid PORT", self.serverPort + " is an invalid port.  Please enter a valid Port.")
			return

	def exit(self):
		"""Proper exiting and resource management"""
		if tkMessageBox.askyesno("Quit?", "Are you sure you want to exit?"):
			self.quit()

	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.loadPictures()
		self.loadQueue()
		self.createWidgets()
		self.grid()

if __name__ == "__main__":
	app = Application()
	app.master.title("Tel Server v 0.1")
	app.master.maxsize(800, 600)
	#app.master.config(menu=app.appMenu)
	app.master.protocol("WM_DELETE_WINDOW", app.exit)
	app.master.wm_iconbitmap('../tel.ico')
	app.mainloop()

	