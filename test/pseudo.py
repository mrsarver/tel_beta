""" Pseudocode For Tel v0.0.0.1
	Author: M.R. Sarver
	Date-Authored: 12 March 2014
"""

from matplotlib import pyplot as plt
from threading import *
from tkinter import *
import tkMessageBox
import numpy as np
import cv2

class Application(Frame):
	"""Handles construction and implementation of GUI"""

	def newCall(self):
	"""get thread from pool, gives thread functions to run"""
	def endCall(self):
	"""joins thread, ends call"""
	def exit(self):
	"""if thread exists, calls endCall().  kills app"""
	def createWidgets(self):
	"""adds buttons, labels, text boxes, etc"""
	def __init__(self):
	"""called when new Application is created"""
		#setup thread pool

class VideoCapture():
"""Handles capture of video"""
	
	def getFrame(self):
	"""returns frame from camera"""
	def getCamera(self):
	"""returns camera ID"""
	def printFrame(self):
	"""prints a frame to screen"""
	def __init__(self):
	"""called when new VideoCapture is created"""

class Connection():
"""Wrapper for Thread - Handles connection to peer"""

	def connectIP(self):
	"""initializes UDP connection to IP"""
	def disconnect(self):
	"""closes UDP connection"""
	def sendFrame(self):
	"""sends a frame over the connection"""
	def recFrame(self):
	"""receive a frame from the connection"""
	def mainloop(self):
	"""the main work loop of the video call"""
	def __init__(self):
	"""called when new Connection is created"""
		#an instance of the VideoCapture class

if __name__ == "___main__":
	#an instance of the Application class()
	#start applications inherited mainloop
