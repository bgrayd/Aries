from motor import motor
import threading

#constants
FRONTPING=0
RIGHTPING=1
REARPING=2
LEFTPING=3
LEFTWHEELPING=4
RIGHTWHEELPING=5
CONVEYORBELT=6
LEFTWHEEL=7
RIGHTWHEEL=8
CONVEYORTILT=9
HOPPERMOTOR=10

WHEELPINGNORMAL=5 #will need to change test
WHEELPINGDELTA=1 #will need to change test
CONVEYORBELTSPEED = 75 #will need to change test
HOPPERSPEED = 50 #will need to change test
CONVEYORTILTSPEEDFORWARD = 50 #will need to change test
CONVEYORTILTSPEEDBACK = -CONVEYORTILTSPEEDFORWARD

def main():
    deviceDrivers={}
    thing = motor(10)
    while(1):
        thing.writePercent_Master(50)
        
    while(1):
        if userInput == "f":
            deviceDrivers[LEFTWHEEL].writePercent_Master(50)
            deviceDrivers[RIGHTWHEEL].writePercent_Master(750)
            time.sleep(2)
        if userInput == "b":
            deviceDrivers[LEFTWHEEL].writePercent_Master(-75)
            deviceDrivers[RIGHTWHEEL].writePercent_Master(-75)
            time.sleep(2)
        if userInput == "tr":
            deviceDrivers[LEFTWHEEL].writePercent_Master(75)
            deviceDrivers[RIGHTWHEEL].writePercent_Master(25)
            time.sleep(2)
        if userInput == "tl":
            deviceDrivers[LEFTWHEEL].writePercent_Master(25)
            deviceDrivers[RIGHTWHEEL].writePercent_Master(75)
            time.sleep(3)
        if userInput == "90r":
            deviceDrivers[LEFTWHEEL].writePercent_Master(75)
            deviceDrivers[RIGTHWHEEL].writePercent_Master(-75)
            time.sleep(3)
        if userInput == "90l":
            deviceDrivers[LEFTWHEEL].writePercent(-75)
            deviceDrivers[RIGHTWHEEL].writePercent(75)
        if userInput == "c":
            deviceDrivers[CONVEYORBELT].writePercent_Master(CONVEYORBELTSPEED)
        else:
            deviceDrivers[CONVEYORBELT].writePercent_Master(0)
        if userInput == "t":
            deviceDrivers[CONVERYORTILT].writePercent_Master(CONVERYORTILTSPEEDBACK)
            time.sleep(5)
        if userInput == "d":
            deviceDrivers[HOPPERMOTOR].writePercent_Master(HOPPERSPEED)
            time.sleep(10)
            deviceDrivers[HOPPERMOTOR].writePercent_Master(0)
        userInput = input("Enter a command: ")
    time.sleep(.1)
    
main()
