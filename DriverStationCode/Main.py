import time
import math
from legopi.lib import xbox_read
import RPi.GPIO as GPIO
import socket
import sys
import threading


HOST, PORT = "192.168.1.101", 1313


SW1 = 7
SW2 = 8
SW3 = 11
SW4 = 22

JOYSTICKMAX = 32768
JOYSTICKSCALAR = math.log10(JOYSTICKMAX)

xboxValues = {"X1":0, "Y1":0, "X2":0, "Y2":0, "guide":0, "A":0, "B":0, "LT":0, "RT":0}

GPIO.setmode(GPIO.BCM)

GPIO.setup(SW1, GPIO.input)
GPIO.setup(SW2, GPIO.input)
GPIO.setup(SW3, GPIO.input)
GPIO.setup(SW4, GPIO.input)

def main():
    updater = threading.Thread(target=xboxInputUpdater, args=())
    updater.start()
    while(True):   
        if((GPIO.input(SW1) or GPIO.input(SW2)) and (GPIO.input(SW3) or GPIO.input(SW4))):
            teleopCycle()
        elif(GPIO.input(SW1) or GPIO.input(SW2)):
            autoCycle()
        time.sleep(.001)


def teleopCycle():
    global xboxValues
    data = "teleop~"
    data += xboxValues["X1"] + "!"
    data += xboxValues["Y1"] + "@"
    data += xboxValues["X2"] + "#"
    data += xboxValues["Y2"] + "$"
    data += xboxValues["guide"] + "%"
    data += xboxValues["A"] + "^"
    data += xboxValues["B"] + "&"
    data += xboxValues["LT"] + "*"
    data += xboxValues["RT"] + "("
    sock.sendto(data, (HOST,PORT))
    

def autoCycle():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto("auto\n",(HOST,PORT))

def xboxInputUpdater():
    global xboxValues
    for event in xbox_read.event_stream(deadzone=12000):
        if event.key=='X1' or event.key=='X2' or event.key=='Y1' or event.key=='Y2':
            value = math.log10(math.fabs(event.value))/JOYSTICKSCALAR * event.value/math.fabs(event.value)
            xboxValues[event.key] = value
        elif event.key=="LT" or event.key=="RT":
            value = (event.value>=128)
            xboxValues[event.key] = value
        else:
            xboxValues[event.key] = event.value
