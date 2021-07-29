# this is the main file
# it handles:
# 1. sending tello.send_rc_control(whatever) commands
# 2. receiving and storing images from the camera
# 3. starting and stopping other threads

# import block
from djitellopy import Tello
import cv2
from odometry import odometry
from threading import Thread
from image_processing import *
from path_following import *

# declaring objects
odo = odometry()
tello = Tello()
cvLoop = cvLoop()
path = path()

tello.connect()
tello.streamon()

# * tello.takeoff() #add when ready
print('here')
# threads
odoThread = Thread(target=odo.startOdometry)
cvThread = Thread(target=cvLoop.imageProcessing, args=[tello])

print('here')
odoThread.start()
cvThread.start()

while(True):
    odo.setMarkers(cvLoop.odoFormat())
    path.setPoints(list(odo.markers.values()))
    direction = followPath(path.getPath(), odo.getPos(), 20, 1)
    tello.send_rc_control(int(direction[0]), int(
        direction[1]), int(direction[2]), 0)
