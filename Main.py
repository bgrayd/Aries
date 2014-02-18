import threading, subprocess, math
import ping_sensor, motors

#constants
FRONTPING=0
RIGHTPING=1
REARPING=2
LEFTPING=3
LEFTWHEELPING=4
RIGHTWHEELPING=5

WHEELPINGNORMAL=5 #will need to change test
WHEELPINGDELTA=1 #will need to change test



def main():    
    #initialize everything

    #list for storing external I/O, external_updater will update to/from this
    externals=[] #will depend on what sensors are used

    #list of device driver objects created
    deviceDrivers={}

    #initialize the drivers for each device

    
    #launches the threads
    #threading.Thread(target=functionName, args=())
    threading.Thread(target=external_updater, args=(externals))
    threading.Thread(target=location_tracking, args=(deviceDrivers))


    #main code
    while(1): #will need to be changed
        orientation()
        toDigArea()
        Dig()
        toDumpArea()
        dump()


def external_updater(externals):
    #cycle through the externals updating them
    #some will be inputs and some will be outputs

def location_tracking(deviceDrivers):
    #uses the accelerameter to keep track of its position



def orientation():
    #minimize two adjacent ping sensors' distance


    #turn to face dig end
    
def toDigArea():
    #will need to add code to keep it mostly facing the correct direction
    leftPing=deviceDrivers[LEFTWHEELPING]
    rightPing=deviceDrivers[RIGHTWHEELPING]
    leftWheel=deviceDrivers[LEFTWHEEL]
    rightWheel=deviceDrivers[RIGHTWHEEL]
    while(!inDigArea()):
        leftDist = leftPing.readCm()
        rightDist = rightPing.readCm()
        deltaLeft = math.fabs(leftDist-WHEELPINGNORMAL)
        deltaRight = math.fabs(rightDist-WHEELPINGNORMAL)

        if(deltaLeft < WHEELPINGDELTA):
            
        
def Dig():

    
def toDumpArea():

    
def dump():


def inDigArea():
    #use location tracking and ping sensors to tell if it is in the digging area


main()
    
