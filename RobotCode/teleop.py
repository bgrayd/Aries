import time
import math
import socket
import sys
import threading

WHEELPINGNORMAL=5 #will need to change test
WHEELPINGDELTA=1 #will need to change test
CONVEYORBELTSPEED = 75 #will need to change test
HOPPERSPEED = 50 #will need to change test
CONVEYORTILTSPEEDFORWARD = 50 #will need to change test
CONVEYORTILTSPEEDBACK = -CONVEYORTILTSPEEDFORWARD


HOST, PORT = "192.168.1.101", 1313

JOYSTICKMAX = 32768
JOYSTICKSCALAR = math.log10(JOYSTICKMAX)

xboxValues = {"X1":0, "Y1":0, "X2":0, "Y2":0, "guide":0, "A":0, "B":0, "LT":0, "RT":0}

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto("auto\n",(HOST,PORT))

def main():
    while(True):   
        if True:
            teleopCycle()
        else:
            if(GPIO.input(SW1) or GPIO.input(SW2)):
                autoCycle()
        time.sleep(.001)


def teleopCycle():
    global xboxValues
    data = "tele~"
    data += str(xboxValues["X1"]) + "!"   #ignore
    data += str(xboxValues["Y1"]) + "@"   #left wheel
    data += str(xboxValues["X2"]) + "#"   #ignore
    data += str(xboxValues["Y2"]) + "$"   #right wheel
    data += str(xboxValues["guide"]) + "%"  #switch modes?
    data += str(xboxValues["A"]) + "^"    #collect (1 or 0)
    data += str(xboxValues["B"]) + "&"    #dump   (1 or 0)
    data += str(xboxValues["LT"]) + "*"   #tilt backwards (1 or 0)
    data += str(xboxValues["RT"]) + "("   #tilt forwards  (1 or 0)
    sock.sendto(data, (HOST,PORT))
    

updater = threading.Thread(target=main, args=())
updater.start()

while(1):
    userInput = input("Enter a command: ")
    if userInput == "f":
        xboxValues["Y1"] = 75
        xboxValues["Y2"] = 75
        time.sleep(2)
    if userInput == "b":
        xboxValues["Y1"] = -75
        xboxValues["Y2"] = -75
        time.sleep(2)
    if userInput == "tr":
        xboxValues["Y1"] = 75
        xboxValues["Y2"] = 25
        time.sleep(2)
    if userInput == "tl":
        xboxValues["Y1"] = 25
        xboxValues["Y2"] = 75
        time.sleep(3)
    if userInput == "90r":
        xboxValues["Y1"] = 75
        xboxValues["Y2"] = -75
        time.sleep(3)
    if userInput == "90l":
        xboxValues["Y1"] = -75
        xboxValues["Y2"] = 75
    if userInput == "c":
        xboxValues["A"] = CONVEYORBELTSPEED
    else:
        xboxValues["A"] = 0
    if userInput == "tf":
        xboxValues["RT"] = CONVEYORTILTSPEEDFORWARD
        time.sleep(5)
    if userInput == "tb":
        xboxValues["LT"] = CONVEYORTILTSPEEDBACK
    if userInput == "d":
        xboxValues["B"] = HOPPERSPEED
        time.sleep(10)
        xboxValues["B"] = 0
    userInput = input("Enter a command: ")
    time.sleep(.1)
