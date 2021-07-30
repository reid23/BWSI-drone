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
from time import sleep
import time

# declaring objects
odo = odometry()
tello = Tello()
cvLoop = cvLoop()
path = path()

tello.connect()
tello.streamon()

startPos = [0, 0, 0]


tello.takeoff()  # add when ready
tello.move_up(50)


# threads
odoThread = Thread(target=odo.startOdometry)
cvThread = Thread(target=cvLoop.imageProcessing, args=[tello])

odoThread.start()
cvThread.start()

try:
    while(True):
        print('here')
        odo.setMarkers(cvLoop.odoFormat())
        path.setPoints(
            [[0.0, 0.0, 0.0]] + list(np.array(list(odo.getRings().values()))))
        direction = followPath(path.getPath(), odo.getPos(), 20, 0.5)
        tello.send_rc_control(int(direction[0]), int(
            direction[1]), int(direction[2]), 0)
        print(odo.getPos())
        #tello.send_rc_control(lr, fb, ud, yaw)
        sleep(1/30)
except KeyboardInterrupt:
    tello.land()
    odo.stopOdometry()
    exit(0)
