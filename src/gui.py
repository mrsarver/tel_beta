import numpy as np
import cv2
from matplotlib import pyplot as plt
from Tkinter import *
import tkMessageBox

class Application(Frame):
	def createWidgets(self):
		self.QUIT = Button(self)
		self.QUIT['text'] = "quit"
		self.QUIT['command'] = self.exit

		self.NEW = Button(self)
		self.NEW['text'] = "New Call to IP"
		self.NEW['command'] = self.newCall

		self.END = Button(self)
		self.END['text'] = "End Call"
		self.END['command'] = self.endCall

		self.QUIT.pack({'side':'left'})
		self.NEW.pack({'side':'left'})
		self.END.pack({'side':'left'})

	def newCall(self):
		if not self.check:
			tkMessageBox.askokcancel("New Call to IP",  "DUDE ENTER AN IP ADDRESS BRO!")
			self.log.write("tel: call message box opened\n")
			self.check += 1
		else:
			self.log.write("tel error: must end active call first\n")

	def endCall(self):
		if (self.check):
			self.log.write("tel: current call ended\n")
			self.check -= 1
		else:
			self.log.write("tel error: no active calls\n")

	def exit(self):
		if tkMessageBox.askokcancel("Quit?", "Are you sure you want to exit.  This will end any calls you are making."):
			if (self.check):
				self.log.write("tel: current call ended\n")
				self.check -= 1
			self.log.write("tel: goodbye...\n")
			self.log.close()
			self.quit()


	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.check = 0
		self.pack()
		self.createWidgets()
		self.log = open('log.txt','w')
		self.log.write("~~~ Welcome to Tel v0.0.0.1 ~~~\n")

if __name__ == "__main__":
	root = Tk()
	root.title("Tel v0.0.0.1")
	app = Application(master=root)
	#bug site 1 - closing the window - close it with quit for now
	root.protocol("WM_DELETE_WINDOW", app.exit)
	#root.wm_iconbitmap(bitmap = "")
	app.mainloop()

###############################################################################
#PROGRAM START
###############################################################################
#
# In main
# Initialize TK inter through wrapper class - let mainloop do its thing
# Draw gui, startup buttons (spawn thread/child process), button functions, main method
#
# Interface has 2 buttons: - Start New Chat - Quit"
#
# Start new chat opens message box (input src ip and button to start)"
#	REMEMBER: This message is a dummy message for now"
#
# Starts OpenCV video capture in new thread, accessible through wrapper class
#		-New thread handles internet connection
#		-client-server (it'll be easier)
#			-peer to peer later gater
#
# Wrapper class functions:
#	1. Get Frame
#	2. Send Frame
#	3. Recieve Frame
#	4. Show recieved Frame
#	5. Has main method
#
# Connection Class:
# Opens UDP/TCP connection to client PROGRAM
#	1. Open Connection
#	2. Close Connection
#	3. Output frame to TCP Connection
#	4. Recieve frame to TCP Connection
#
###############################################################################
#PROGRAM END
###############################################################################