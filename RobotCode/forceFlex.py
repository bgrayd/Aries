from grovepi import *

class forceFlex():
	def __init__(port, sensors, semaphore):
		self.port = port
		self.sensors = sensors
		self.raw = -1
		self.semaphore = semaphore
		self.caledAmount = 1000 #may not be correct, but best I can do without the robot on hand

	def getRaw():
		return self.raw

        def getFull():
            self.getRaw()
            return self.raw <= self.caledAmount

	def update():
		self.raw = analogRead(self.port)
		return self.raw
		
	def readRaw():
		self.update()
		return self.getRaw()
