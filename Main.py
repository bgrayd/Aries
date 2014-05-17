import threading, subprocess, math
import ping_sensor, motor

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
	pass


def location_tracking(deviceDrivers):
    #uses the accelerometer to keep track of its position
	pass


def orientation():
    #minimize two adjacent ping sensors' distance
    leftPing=deviceDrivers[LEFTPING]
    rightPing=deviceDrivers[RIGHTPING]
    frontPing=deviceDrivers[FRONTPING]
    rearPing=deviceDrivers[REARPING]
    leftWheel=deviceDrivers[LEFTWHEEL]
    rightWheel=deviceDrivers[RIGHTWHEEL]

    '''
    for turning, basically use the left or right ping as a reference
    point. The the robot turns until the front ping sensor distance is 
    relatively close to where the left or right ping was at. 20 is just 
    being used as an arbitrary value and will likely have to be changed.
    '''
    def turnLeft():
        turnt = leftPing.readCm()
        frontDist = 0
        while frontDist > turnt + 20 or frontDist < turnt - 20:
            rightWheel.writePercent(75)
            leftWheel.writePercent(-75)
            frontDist = frontPing.readCm()

    def turnRight():
        turnt = rightPing.readCm()
        frontDist = 0
        while frontDist > turnt + 20 or frontDist < turnt -20:
            rightWheel.writePercent(-75)
            leftWheel.writePercent(75)
            frontDist = frontPing.readCm()

    aligned = False
    '''
    not really sure how well this would work. any other suggestions on minimizing the distances with the pings? 
    I think the delta variables were used properly
    '''
    while aligned != True:
        rightWheel.writePercent(75)
        leftWheel.writePercent(-75)
        leftDist = leftPing.readCm()
        rightDist = rightPing.readCm()
        deltaLeft = math.fabs(leftDist-WHEELPINGNORMAL)
        deltaRight = math.fabs(rightDist-WHEELPINGNORMAL)
        if deltaLeft > 70 or deltaRight > 70:   #arbitrary value that indicates when robot is no longer facing a wall at an angle
            aligned = True
        else:
            aligned = False
    #roughly center horizontally
    distances = []
    frontDist = frontPing.readCm()
    rightDist = rightPing.readCm()
    rearDist = rearPing.readCm()
    leftDist = leftPing.readCm()
    distances.append(frontDist)
    distances.append(rightDist)
    distances.append(rearDist)
    distances.append(leftDist)
    maxDist = max(distances)

    distDiff = 0   #indicates when robot is roughly centered on the field
    if frontDist is maxDist:
        if leftDist > rightDist:
            turnLeft()
            while distDiff > 30:  #arbitray, determine later
                leftWheel.writePercent(75)
                rightWheel.writePercent(75)
                distDiff = fabs(frontPing.readCm()-backPing.readCm())
            turnRight()
        else:
            turnRight()
            while distDiff > 30:
               leftWheel.writePercent(75)
               rightWheel.writePercent(75)
               distDiff = fabs(frontPing.readCm()-backPing.readCm())
            turnLeft()

    if rightDist is maxDist:
        if frontDist > rearDist:
            while distDiff > 30:
                leftWheel.writePercent(75)
                rightWheel.writePercent(75)
                distDiff = fabs(frontPing.readCm()-backPing.readCm())
            turnRight()
        else:
            while distDiff > 30:
                leftWheel.writePercent(-75)
                rightWheel.writePercent(-75)
                distDiff = fabs(frontPing.readCm()-backPing.readCm())
            turnRight()
    
    if rearDist is maxDist:
        if rightDist > leftDist:
            turnRight()
            while distDiff > 30:
                leftWheel.writePercent(75)
                rightWheel.writePercent(75)
                distDiff = fabs(frontPing.readCm()-backPing.readCm())
            turnRight()
        else:
            turnRight()
            while distDiff > 30:
                leftWheel.writePercent(-75)
                rightWheel.writePercent(-75)
                distDiff = fabs(frontPing.readCm()-backPing.readCm())
            turnRight()
    
    if leftDist is maxDist:
        if frontDist > rearDist:
            while distDiff > 30:
                leftWheel.writePercent(75)
                rightWheel.writePercent(75)
                distDiff = fabs(frontPing.readCm()-backPing.readCm())
            turnLeft()
        else:
            while distDiff > 30:
                leftWheel.writePercent(-75)
                rightWheel.writePercent(-75)
                distDiff = fabs(frontPing.readCm()-backPing.readCm())
            turnLeft()

    
def toDigArea():
    #will need to add code to keep it mostly facing the correct direction
    leftPing=deviceDrivers[LEFTWHEELPING]
    rightPing=deviceDrivers[RIGHTWHEELPING]
    leftWheel=deviceDrivers[LEFTWHEEL]
    rightWheel=deviceDrivers[RIGHTWHEEL]
    while not inDigArea():
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
        else:
            rightWheel.writePercent(25)
            
        if(deltaRight < WHEELPINGDELTA):
            leftWheel.writePercent(75)
        else:
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
            leftWheel.writePercent(digForwardSpeed)
            rightWheel.writePercent(digForwardSpeed)
            conveyor.writePercent(conveyorSpeed)
            if(isFull()):
                break

        #logic for turning 90 degrees
        
        if(isFull()):
            break
            
    

    
def toDumpArea():
	pass
    
def dump():
	pass

#returns a bool
def inDigArea():
    #use location tracking and ping sensors to tell if it is in the digging area
	pass

#returns boolean, if hopper is full
def isFull():
	pass


main()
    
