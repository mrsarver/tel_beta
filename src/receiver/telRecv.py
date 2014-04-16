from Tkinter import *
from PIL import Image, ImageTk
import tkMessageBox
import Queue
import receiver

class Application(Frame):
	def createWidgets(self):
		"""Construct Graphical User Interface"""
		#default skype port is 23399
		self.receiverPort = IntVar()
		self.PORTLABEL = Label(self, text="LISTEN ON PORT: ")
		self.PORTENTRY = Entry(self, width=5, textvar=self.receiverPort)
		self.BUTTONNEW = Button(self, text="Start listening", command=self.startReceiver)
		self.BUTTONEND = Button(self, text="End listening", command=self.endReceiver)
		self.PICTFRAME = Label(self, image=self.picture)

		self.PORTLABEL.grid(row=0, column=0)
		self.PORTENTRY.grid(row=0, column=1)
		self.BUTTONNEW.grid(row=0, column=2)
		self.BUTTONEND.grid(row=0, column=3)
		self.PICTFRAME.grid(row=1, column=0, columnspan=4)

		self.appMenu = Menu(self)
		self.fileMenu = Menu(self.appMenu, tearoff=0)
		self.fileMenu.add_command(label="Exit", command=self.exit)
		self.appMenu.add_cascade(label="File", menu=self.fileMenu)

		self.PORTENTRY.focus_set()
		pass

	def loadPictures(self):
		"""Loads the initial tel image"""
		self.picture = ImageTk.PhotoImage(Image.open("../../img/telsmall.png"))

	def loadQueue(self):
		"""Initialize a queue for image storage"""
		self.frameQueue = Queue.Queue()

	def startReceiver(self):
		"""Initiate the receiver"""
		self.isRunning = True
		self.receiverPort = self.PORTENTRY.get()
		self.receiverPort = int(self.receiverPort)

		if self.receiverPort < 1024 or self.receiverPort > 65535:
			tkMessageBox.showerror("Invalid PORT", self.receiverPort + " is an invalid port.  Please enter a valid Port.")
			return False

		self.receiverThread = receiver.Receiver(self.receiverPort, self.frameQueue)
		self.receiverThread.start()

		while self.isRunning:
			if not self.frameQueue.empty():
				message = self.frameQueue.get()
				im = Image.fromstring('RGB', (640, 480), message)
				im = ImageTk.PhotoImage(image = im)
				self.PICTFRAME["image"] = im
				self.PICTFRAME._image_cache = im
			else:
				continue

			self.update()

		self.frameQueue.queue.clear()
		self.receiverThread.isRunning = False
		return True

	def endReceiver(self):
		"""Kill the receiving of frames"""
		self.isRunning = False
		self.PICTFRAME["image"] = self.picture

	def exit(self):
		"""Proper exiting and resource management"""
		if tkMessageBox.askyesno("Quit?", "Are you sure you want to exit?"):
			self.endReceiver()
			self.quit()

	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.loadPictures()
		self.loadQueue()
		self.createWidgets()
		self.grid()

if __name__ == "__main__":
	app = Application()
	app.master.title("Tel Receiver v 0.2")
	app.master.maxsize(800, 600)
	app.master.config(menu=app.appMenu)
	app.master.protocol("WM_DELETE_WINDOW", app.exit)
	app.master.wm_iconbitmap('../../img/tel.ico')
	app.mainloop()
