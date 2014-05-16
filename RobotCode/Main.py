import threading, subprocess, math
import ping_sensor, motors

#constants
FRONTPING=0
RIGHTPING=1
REARPING=2
LEFTPING=3
LEFTWHEELPING=4
RIGHTWHEELPING=5
CONVEYORBELT=6

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


    #roughly center horizontally

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
        #add code to make sure it doesn't hit walls
        #check to see if conveyor assembly up
        #also need to add an if to make sure it does not get too far off target
        #will probably need to change to avoid jumpiness
        #debug
        if(deltaLeft < WHEELPINGDELTA):
            rightWheel.writePercent(75)
        else
            rightWheel.writePercent(25)
            
        if(deltaRight < WHEELPINGDELTA):
            leftWheel.writePercent(75)
        else
            leftWheel.writePercent(-25)
            
        
def Dig():
    digForwardSpeed = 100
    digTurnSpeed = 75
    conveyorSpeed = 50
    turnDistance = 7
    DistanceAwayFromWallFront = 50 #cm width/length of robot plus 2, need to get actual value
    DistanceAwayFromWallBack
    #debug

    leftPing=deviceDrivers[LEFTPING]
    rightPing=deviceDrivers[RIGHTPING]
    frontPing=deviceDrivers[FRONTPING]
    rearPing=deviceDrivers[REARPING]
    leftWheel=deviceDrivers[LEFTWHEEL]
    rightWheel=deviceDrivers[RIGHTWHEEL]
    conveyor=deviceDrivers[CONVEYORBELT]

    while(True):
        #digging from navigation area to wall
        while(frontPing < DistanceFromWallFront):
          leftWheel.writePercent(digForwardSpeed)
            rightWheel.writePercent(digForwardSpeed)
            conveyor.writePercent(conveyorSpeed)
            if(isFull()):
                break
            
        if(isFull()):
            break

        #logic for turning 90 degrees
        
        if(isFull()):
            break
        
        #digging from wall to navigation area
        while(backPing < DistanceAwayFromWallBack):
            leftWheel.writePercent(diForwardSpeed)
            rightWheel.writePercent(digForwardSpeed)
            conveyor.writePercent(conveyorSpeed)
            if(isFull()):
                break

        #logic for turning 90 degrees
        
        if(isFull()):
            break
            
    

    
def toDumpArea():

    
def dump():


#returns a bool
def inDigArea():
    #use location tracking and ping sensors to tell if it is in the digging area


#returns boolean, if hopper is full
def isFull():


main()
    
