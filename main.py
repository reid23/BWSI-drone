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
import collections

startTime = time.time()
# declaring objects
odo = odometry()
tello = Tello()
cvLoop = cvLoop()
path = path()

tello.connect()
tello.streamon()

startPos = [0, 0, 0]


tello.takeoff()  # add when ready


# threads
odoThread = Thread(target=odo.startOdometry)
cvThread = Thread(target=cvLoop.imageProcessing, args=[tello])

odoThread.start()
cvThread.start()

# In [1]: import collections

# In [2]: d = {2:3, 1:89, 4:5, 3:0}

# In [3]: od = collections.OrderedDict(sorted(d.items()))

# In [4]: od
# Out[4]: OrderedDict([(1, 89), (2, 3), (3, 0), (4, 5)])


try:
    counter = 0
    while(True):
        odo.setMarkers(cvLoop.odoFormat())
        od = collections.OrderedDict(sorted(odo.getRings().items()))
        points = [[0.0, 0.0, 0.0]] + list(od.values())
        path.setPoints(points)
        direction = followPath(path.getPath(), odo.getPos(), 10, 1, odo)
        tello.send_rc_control(int(direction[0]), int(
            direction[2]), int(direction[1]), 0)
        # tello.send_rc_control(lr, fb, ud, yaw)
        sleep(1/30)
except KeyboardInterrupt:
    tello.land()
    odo.stopOdometry()
    exit(0)
tello.move_forward(50)
tello.land()
