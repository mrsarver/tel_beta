#!/usr/bin/env python
import numpy as np
import cv2

class Camera(object):
	def __init__(self):
		self.device = cv2.VideoCapture(0)
		self.color = None
	def __name__(self):
		return "Camera"
	def __str__(self):
		#returns string representation - camera name?
		pass
	def nextFrame(self):
		#this frame cannot be altered, gotta copy it
		return self.device.read()

def function():
	cam = Camera()
	while(True):
		ret, frame = cam.nextFrame()
		cv2.imshow('frame', frame)
		#requires at least a millisecond of delay otherwise no updated video - threads?
		if (cv2.waitKey(1) == ord('q')):
			print frame
			break
	
	cam.device.release()
	cv2.destroyAllWindows()
