from grovepi import *

class pingDigi():
    def __init__(port, sensors, semaphore):
        self.port = port
        self.sensors = sensors
        self.raw = -1
        self.semaphore

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
        self.raw = ultrasonicRead(self.port)
        return self.raw

