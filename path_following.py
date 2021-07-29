# converts path and odometry data, using a PID loop and a path following algorithm (currently pure pursuit)
# to generate send_rc_control values that can be sent by main.py

import scipy.interpolate
import numpy as np
from math import sqrt
from numba import njit


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

    def recalc(self):
        for i in self.points:
            self.x.append(i[0])
            self.y.append(i[1])
            self.z.append(i[2])
        try:
            self.pathxy = scipy.interpolate.CubicSpline(
                self.x, self.y, bc_type='clamped')
            self.pathyz = scipy.interpolate.CubicSpline(
                self.y, self.z, bc_type='clamped')

            for i in range(max(self.y)):  # convert splines to arrays of points
                self.path1.append(self.pathxy(i))
                self.path2.append(self.pathyz(i))

            # convert arrays of 2d points to one array of 3d points
            for i in range(len(self.path1)-1):
                self.path.append(self.path1[i].append(self.path2[i][1]))

        except ValueError:
            print("not enough points for a path")

    def addPoint(self, point):
        self.points.append(point)
        self.recalc()

    def setPoints(self, points):
        self.points = points

    def getPath(self):
        return self.path


def distance(a, b):
    return sqrt(((a[0]-b[0])**2)+((a[1]-b[1])**2)+((a[2]-b[2])**2))


def followPath(path, curPos, dist, kp):
    dists = []
    for i in path:
        dists.append(distance(curPos, i))
    closest = 999999999999999999999
    closestNum = 0
    counter = 0
    # get target point
    for i in dists:
        # make sure it's closer, and make sure it's the front point and not the back one
        if i <= closest and path[counter][1] > curPos[1]:
            closest = i
            closestNum = counter
        counter += 0

    # so the target point is
    try:
        targetPoint = np.array(path[closestNum])
    except IndexError:
        print('no points left')
        targetPoint = curPos
    # get direction to target

    direction = np.subtract(targetPoint, np.array(curPos))

    return direction*kp
