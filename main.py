# this is the main file
# it handles:
# 1. sending tello.send_rc_control(whatever) commands
# 2. receiving and storing images from the camera
# 3. starting and stopping other threads

from djitellopy import Tello
import cv2
from odometry import odometry
from threading import Thread

odo = odometry()

t = Thread(target=odo.startOdometry())

t.start()
