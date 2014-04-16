from Tkinter import *
from PIL import Image, ImageTk
import tkMessageBox
import Queue
import regextel
import cv2
import sender

class Application(Frame):
	def createWidgets(self):
		"""Construct Graphical User Interface"""
		self.IPLABEL = Label(self, text = "Dest IPv4 Address:")
		self.IPENTRY = Entry(self, width=15)
		self.PORTLABEL = Label(self, text = "Dest Port:")
		self.PORTENTRY = Entry(self, width=5)
		self.BUTTONNEW = Button(self, text="New Call to IP", command=self.newCall)
		self.BUTTONEND = Button(self, text="End Call", command=self.endCall)
		self.BUTTONXIT = Button(self, text="Quit", command=self.exit)
		self.PICTFRAME = Label(self, image=self.picture)
		self.LISTBXLOG = Listbox(self, height=2, relief=SUNKEN, background="white")
		self.SCROLLLOG = Scrollbar(self, command=self.LISTBXLOG.yview)
		self.LISTBXLOG.configure(yscrollcommand=self.SCROLLLOG.set)
		self.IPENTRY.focus_set()

		self.IPLABEL.grid(row=0, column=0)
		self.IPENTRY.grid(row=0, column=1)
		self.PORTLABEL.grid(row=0, column=2)
		self.PORTENTRY.grid(row=0, column=3)
		self.BUTTONNEW.grid(row=1, column=0, sticky=W+E)
		self.BUTTONEND.grid(row=1, column=1, sticky=W+E)
		self.BUTTONXIT.grid(row=1, column=2, columnspan=4, sticky=W+E)
		self.PICTFRAME.grid(row=2, column=0, columnspan=4)
		self.LISTBXLOG.grid(row=3, column=0, columnspan=3)
		self.SCROLLLOG.grid(row=3, column=3)
		self.grid_rowconfigure(3, weight=1)

		self.appMenu = Menu(self)
		self.fileMenu = Menu(self.appMenu, tearoff=0)
		self.fileMenu.add_command(label="New Call", command=self.newCall)
		self.fileMenu.add_command(label="End Call", command=self.endCall)
		self.fileMenu.add_separator()
		self.fileMenu.add_command(label="Exit", command=self.exit)
		self.editMenu = Menu(self.appMenu, tearoff=0)
		self.editMenu.add_command(label="Placeholder", command=None)
		self.appMenu.add_cascade(label="File", menu=self.fileMenu)
		self.appMenu.add_cascade(label="Edit", menu=self.editMenu)

	def newCall(self):
		"""Initialize a new call to a specified IP"""
		ip = self.IPENTRY.get()
		destPort = IntVar()
		destPort = self.PORTENTRY.get()
		destPort = int(destPort)

		if regextel.isValidIP(ip) == None or ip == "0.0.0.0":
			tkMessageBox.showerror("Invalid IPv4 address", ip + "is an invalid IPv4 address.  Please enter a valid IPv4 address.")
			self.IPENTRY.focus_set()
			self.IPLABEL["fg"] = "red"
			return False

		if destPort < 1024:
			tkMessageBox.showerror("Invalid PORT", destPort + " is an invalid port.  Please enter a valid Port.")


		self.IPLABEL["fg"] = "black"

		self.callActive = True
		cap = cv2.VideoCapture(0)
		self.senderThread = sender.Sender(ip, destPort, self.frameQueue)
		self.senderThread.start()
		while self.callActive:
			ret, img = cap.read()
			img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
			img = Image.fromarray(img)
			message = img.tostring()
			img = ImageTk.PhotoImage(image=img)
			self.PICTFRAME["image"] = img
			self.frameQueue.put(message)
			self.update()
		cap.release()

	def endCall(self):
		"""End the current call, returns True on success, False on failure"""
		if self.callActive:
			self.callActive = False
			self.PICTFRAME["image"] = self.picture
			self.senderThread.isRunning = False
			self.senderThread.join()

	def exit(self):
		"""Proper exiting and resource management"""
		if tkMessageBox.askyesno("Quit?", "Are you sure you want to exit?  This will end any calls you are making."):
			self.endCall()
			self.quit()

	def loadPictures(self):
		"""Loads the initial tel image"""
		self.picture = ImageTk.PhotoImage(Image.open("../../img/telsmall.png"))

	def loadQueue(self):
		"""Initialize a queue for image storage"""
		self.frameQueue = Queue.Queue()

	def loadVar(self):
		"""Loads any variables required for the application"""
		self.callActive = False
		self.maxLogSize = 100

	def LogWrite(self, message):
		"""Writes a message to the log box"""
		self.LISTBXLOG.insert(END, message)
		if self.LISTBXLOG.size() > self.maxLogSize:
			self.LISTBXLOG.delete(0)
		pass

	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.loadVar()
		self.loadPictures()
		self.loadQueue()
		self.createWidgets()
		self.grid()

if __name__ == "__main__":
	app = Application()
	app.master.title("Tel Sender v 0.2")
	app.master.config(menu=app.appMenu)
	app.master.protocol("WM_DELETE_WINDOW", app.exit)
	app.master.wm_iconbitmap('../../img/tel.ico')
	app.mainloop()