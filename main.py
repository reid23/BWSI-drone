# this is the main file
# it handles:
# 1. sending tello.send_rc_control(whatever) commands
# 2. receiving and storing images from the camera
# 3. starting and stopping other threads

#import block
from djitellopy import Tello
import cv2
from odometry import odometry
from threading import Thread
from image-processing import *
from path-following import *

# declaring objects
odo = odometry()
tello = Tello()
cvLoop = CvLoop()
path = Path()

tello.connect()
tello.streamon()

# * tello.takeoff() #add when ready

# threads
odoThread = Thread(target=odo.startOdometry())
cvThread = Thread(target=cvLoop.imageProcessing())
odoThread.start()
cvThread.start()

while(True):
    odo.setMarkers(cvLoop.odoFormat())
    path.setPoints(odo.hoopMarkers)
    direction = followPath(path.getPath(), odo.getPos(), 20, 1)
    tello.send_rc_control(direction[0], direction[1], direction[2], 0)
