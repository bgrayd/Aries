import threading, subprocess, math
import ping_sensor, motors
from UDProboSERVER import *
import Queue

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
ACCMAG = 11

MAXORIENTATIONOFFSET = 25
WHEELPINGNORMAL=5 #will need to change test
WHEELPINGDELTA=1 #will need to change test
CONVEYORBELTSPEED = 75 #will need to change test
HOPPERSPEED = 50 #will need to change test
CONVEYORTILTSPEEDFORWARD = 50 #will need to change test
CONVEYORTILTSPEEDBACK = -CONVEYORTILTSPEEDFORWARD

driverSemaphore = threading.Semaphore()

udpQueue = Queue()

teleop = False
controlInput = {"X1":0, "Y1":0, "X2":0, "Y2":0, "guide":0, "A":0, "B":0, "LT":0, "RT":0}

def main():    
    #initialize everything
    global semaphore
    #list for storing external I/O, external_updater will update to/from this
    externals=[] #will depend on what sensors are used

    #list of device driver objects created
    deviceDrivers={}

    #initialize the drivers for each device

    
    #launches the threads
    #threading.Thread(target=functionName, args=())
    ext_updater = threading.Thread(target=external_updater, args=(externals))
    loc_track = threading.Thread(target=location_tracking, args=(deviceDrivers))
    auto_thread = threading.Thread(target=autonomous, args=())
    UDPServer = threading.Thread(target=UdpRoboServer, args=())
    tele_thread = threading.Thread(target=teleop, args=())

    ext_updater.start()
    loc_track.start()
    UDPServer.start()

    autoStarted = False
    teleStarted = False

    while(1):
        msg = udpQueue.get()
        if(msg[0] == 'a'):
            if(not autoStarted):
                auto_thread.start()
                autoStarted =True
            teleop = False
        elif(msg[0] == 't'):
            parseInput(msg)
            if(not teleStarted):
                tele_thread.start()
                teleStarted =True
            teleop = True
    

def parseInput(msg):
    global controlInput
    pos1=msg.find('~')
    pos2=msg.find('!')
    pos3=msg.find('@')
    pos4=msg.find('#')
    pos5=msg.find('$')
    pos6=msg.find('%')
    pos7=msg.find('^')
    pos8=msg.find('&')
    pos9=msg.find('*')
    pos10=msg.find('(')
    controlInput["X1"]=float(msg[pos1+1,pos2])
    controlInput["Y1"]=float(msg[pos2+1,pos3])
    controlInput["X2"]=float(msg[pos3+1,pos4])
    controlInput["Y2"]=float(msg[pos4+1,pos5])
    controlInput["guide"]=bool(msg[pos5+1,pos6])
    controlInput["A"]=bool(msg[pos6+1,pos7])
    controlInput["B"]=bool(msg[pos7+1,pos8])
    controlInput["LT"]=bool(msg[pos8+1,pos9])
    controlInput["RT"]=bool(msg[pos9+1,pos10])
    


#a collect
#b dump
#triggers for tilt
def teleop():
    global driverSemaphore
    global teleop
    global controlInput
    while(1):
        driverSemaphore.acquire()
        while(teleop):
            if(True):#this will later be for toggling between arcade and tank
                deviceDrivers[LEFTWHEEL].writePercent_Master(controlInput["Y1"])
                deviceDrivers[RIGHTWHEEL].writePercent_Master(controlInput["Y2"])
                if(controlInput["A"]):
                    deviceDrivers[CONVEYORBELT].writePercent_Master(CONVEYORBELTSPEED)
                else:
                    deviceDrivers[CONVEYORBELT].writePercent_Master(0)
                    
                if(controlInput["B"]):
                    deviceDrivers[HOPPERMOTOR].writePercent_Master(HOPPERSPEED)
                else:
                    deviceDrivers[HOPPERMOTOR].writePercent_Master(0)
                    
                if((controlInput["LT"] and controlInput["RT"])or not (controlInput["LT"] and controlInput["RT"])):
                    deviceDrivers[CONVEYORTILT].writePercent_Master(0)
                elif(controlInput["LT"]):
                    deviceDrivers[CONVEYORTILT].writePercent_Master(CONVEYORTILTSPEEDBACK)
                elif(controlInput["RT"]):
                    deviceDrivers[CONVEYORTILT].writePercent_Master(CONVEYORTILTSPEEDFORWARD)
        driverSemaphore.release()
        time.sleep(.1)
                
    

    #autonomous code
def autonomous():
    global driverSemaphore
    while(1): #will need to be changed
        orientation()
        toDigArea()
        Dig()
        toDumpArea()
        dump()


def external_updater(externals):
    #cycle through the externals updating them
    #some will be inputs and some will be outputs
        global deviceDrivers

        for each in deviceDrivers:
            deviceDrivers[each].update()



def location_tracking(deviceDrivers):
    #uses the accelerameter to keep track of its position
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
    while(not inDigArea()):
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

        #logic for turning 180 degrees
        turnLeft(180)
        
        if(isFull()):
            break
        
        #digging from wall to navigation area
        while(backPing < DistanceAwayFromWallBack):
            leftWheel.writePercent(digForwardSpeed)
            rightWheel.writePercent(digForwardSpeed)
            conveyor.writePercent(conveyorSpeed)
            if(isFull()):
                break

        #logic for turning 180 degrees
            turnLeft(180)
        
        if(isFull()):
            break
    '''
    have scoop finish cycle so that extra dirt isn't being carried around
    
    while proximity sensor != True
        run motor for scoop
    '''


def turnLeft(angle):
    newAngle=deviceDrivers[ACCMAG].getHeading()-angle
    if(newAngle<0):
        newAngle+=360
    while(newAngle != deviceDrivers[ACCMAG]):
        deviceDrivers[RIGHTWHEEL].writePercent(-50)
        deviceDrivers[LEFTWHEEL].writePercent(50)

def turnRight(angle):
        newAngle=deviceDrivers[ACCMAG].getHeading()+angle
    if(newAngle>360):
        newAngle-=360
    while(newAngle != deviceDrivers[ACCMAG]):
        deviceDrivers[RIGHTWHEEL].writePercent(50)
        deviceDrivers[LEFTWHEEL].writePercent(-50)

    
def toDumpArea():
    '''
    move backwards until back ping sensor is within a certain range
    '''
    
def dump():
    '''
    have motor run until hopper has attempted to dump 3 times?
    '''


#returns a bool
def inDigArea():
    #use location tracking and ping sensors to tell if it is in the digging area
    if(math.fabs(deviceDrivers[ACCMAG].getCalHeading())<=MAXORIENTATIONOFFSET):
        if(deviceDrivers[frontPing].getCm()<2940):
            return True
    return False


#returns boolean, if hopper is full
def isFull():
    pass



main()
    
