from grovepi import *

class Potentiometer():
	def __init__(port, sensors, semaphore):
		self.port = port
		self.sensors = sensors
		self.raw = -1
		self.semaphore = semaphore

	def getRaw():
		return self.raw

	def getDegrees():
		return self.raw*360/1023

	def update():
		return self.raw = analogRead(self.port)

	def readDegrees():
		self.update()
		return self.getDegrees()
		
	def readRaw():
		self.update()
		return self.getRaw()
