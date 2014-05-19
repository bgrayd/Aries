import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

switches = {"7":GPIO.setup(7, GPIO.input), "8":GPIO.setup(8, GPIO.input),"11":GPIO.setup(11, GPIO.input),"22":GPIO.setup(22, GPIO.input)}

while(True):
    for i in switches:
        if (GPIO.input(int(i))):
            print i
