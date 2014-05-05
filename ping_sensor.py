from grovepi import *

class ping():
    def __init__(port, sensors):
        self.port = port
        self.sensors = sensors
		self.raw = -1

    def readFeet():
        #read it from the sensor port and convert to feet
		self.update()
        return self.getFeet()

    def readCm():
        #read distance from the sensor port and convert to feet
        self.update()
		return self.getCm()

	def getCm():
		return self.raw

	def getFeet():
		return self.raw*2.54/12

	def update():
		return self.raw = ultrasonicRead(self.port)

