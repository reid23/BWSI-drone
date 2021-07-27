# converts path and odometry data, using a PID loop and a path following algorithm (currently pure pursuit)
# to generate send_rc_control values that can be sent by main.py

import scipy
import numpy as np


class path():
    points = []
    x = []
    y = []
    z = []
    pathxy = 0
    pathyz = 0
    path1 = []
    path2 = []
    path = []

    def __init__(self, points):
        self.points = points
        self.recalc()

    def recalc(self):
        for i in points:
            self.x.append(i[0])
            self.y.append(i[1])
            self.z.append(i[2])
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

    def addPoint(self, point):
        self.points.append(point)
        self.recalc()

    def getPath(self):
        return self.path


def followPath(path):
    pass
