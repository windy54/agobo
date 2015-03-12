# lineFollower.py
# developed for 4tronix agobo robot

# runs automacially on power up
# searches for  a black line which the robot straddles
# irleds return False when Black detected
# so do not make it too wide
# mode switch used to shutdown the robot


import agobo, time

def outputModeOnChange(text,newMode,oldMode,labels,fo):
    if oldMode != newMode:
        fo.write( text+labels[newMode]+"\n")
        oldMode = newMode
    return oldMode
    
speed = 30
slowTurn = 25
fastTurn = 75
agobo.init()

# set up some globals
LOOKINGFORLINE = 0
LINESTRADDLED = 1
LEFTEDGEDETECTED = 2
RIGHTEDGEDETECTED = 3
STOP = 4
labels = ["LOOKINGFORLINE ","LINESTRADDLED ","LEFTEDGEDETECTED ","RIGHTEDGEDETECTED ","STOP"]

TIMEOUTCOUNT = 200
mode = LOOKINGFORLINE
oldMode = -1
LETSGO = True

fo=open("linedebug.txt","w")
fo.write("hello"+"\n")

try:
   while LETSGO:
      LineL = agobo.irLeftLine() # False equates to Black detected
      LineR = agobo.irRightLine()
      agobo.setAllLEDs(0) # all off
      if LineL ==True and LineR == True:
         # straight on
         agobo.forward(speed)
      elif LineL==False and LineR==True:
         #left turn
         agobo.spinLeft(speed)
         count = 0
         agobo.setLED(0,1) # left on
         while LineL == False:
            #turn left until led goes off
            LineL = agobo.irLeftLine()
            count=+1
            if count > 50:
              print "count exceeded"
              break
         agobo.forward(speed)
      elif LineL==True and LineR==False:
         #right turn
         agobo.spinRight(speed)
         agobo.setLED(1,1) # right on
         count = 0
         while LineR == False:
            #turn left until led goes off
            LineR = agobo.irRightLine()
            count=+1
            if count > 50:
               print "count exceeded"
               break
         agobo.forward(speed)
      else:
         #both must be false so turn around
         count = 0
         agobo.spinLeft(speed)
         agobo.setLED(0,1) # left on
         while LineL == False:
            #turn left until led goes off
            LineL = agobo.irLeftLine()
            count=+1
            if count > 50:
               print "count exceeded"
               break
         while LineL == True:
            #turn left until led goes on
            LineL = agobo.irLeftLine()
            count=+1
            if count > 50:
               print "count exceeded"
               break
         agobo.forward(speed)
      time.sleep(0.2)

except:
    LETSGO = False
    print "exception"

finally:
    print "finally"
    agobo.cleanup()
    fo.close()
    
