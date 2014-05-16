class motor():
    def __init__(self,port, motors):
        self.port = port
        self.motors = motors

    def writePercent(self,percent):
        if((percent > 100) or (percent < -100))
            return -1
        value = percent + 150 #I know 150 is the middle, and that 250 is possible
        try:
            file1 = open("/dev/servoblaster", "a")
            file1.write(str(self.port)+"="+str(value))
            file1.close()
        except Exception as Ex:
            file1.close()

        
