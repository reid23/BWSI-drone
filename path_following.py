# converts path and odometry data, using a PID loop and a path following algorithm (currently pure pursuit)
# to generate send_rc_control values that can be sent by main.py

import scipy.interpolate
import numpy as np
from math import sqrt
from numba import njit
from math import floor
import time


class path():

    def __init__(self, points=[]):
        self.points = []
        self.x = []
        self.y = []
        self.z = []
        self.pathxy = 0
        self.pathyz = 0
        self.path1 = []
        self.path2 = []
        self.path = []
        self.points = points
        self.recalc()

    # @njit
    def recalc(self):
        self.x = []
        self.y = []
        self.z = []
        for i in self.points:
            self.x.append(i[2])
            self.y.append(i[0])
            self.z.append(i[1])
        try:
            self.pathxy = scipy.interpolate.CubicSpline(
                self.x, self.y, bc_type='clamped')
            self.pathyz = scipy.interpolate.CubicSpline(
                self.x, self.z, bc_type='clamped')

            self.path1 = []
            self.path2 = []
            self.path = []
            # convert splines to arrays of points
            for i in range(int(floor(abs(max(self.x))))):
                self.path1.append(self.pathxy(i))
                self.path2.append(self.pathyz(i))

            # convert arrays of 2d points to one array of 3d points
            for i in range(len(self.path1)):
                self.path.append([])
                self.path[i].append(i)
                self.path[i].append(self.path1[i])
                self.path[i].append(self.path2[i])

        except ValueError:
            print("not enough points for a path")
            # print(e)

    def addPoint(self, point):
        self.points.append(point)
        self.recalc()

    def setPoints(self, points):
        self.points = points
        self.recalc()

    def getPath(self):
        return self.path


@njit
def distance(a, b):
    return sqrt(((a[0]-b[0])**2)+((a[1]-b[1])**2)+((a[2]-b[2])**2))


def followPath(path, curPos, dist, kp):
    dists = []
    path = np.array(path)
    for i in path:
        dists.append(distance(np.array(curPos), i))
    closest = 9999999
    closestNum = 0
    counter = 0
    # get target point
    for i in dists:
        # make sure it's closer, and make sure it's the front point and not the back one
        if i <= closest and path[counter][2] > curPos[2]:
            closest = i
            closestNum = counter
        counter += 1

    # so the target point is
    try:
        targetPoint = np.array(path[closestNum])
        direction = np.subtract(targetPoint[0:3], np.array(curPos))
        return direction*kp
    except IndexError:
        print('no points left')
        targetPoint = curPos
        return [0, 0, 0]
    # get direction to target
