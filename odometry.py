# this file has the odometry class
# it takes in the image from the drone and updates the position array

import numpy as np


class Dictlist(dict):
    def __setitem__(self, key, value):
        try:
            self[key]
        except KeyError:
            super(Dictlist, self).__setitem__(key, [])
        self[key].append(value)


class odometry():
    def __init__(self, knownMarkers={}):
        self.markersDictFixed = Dictlist()
        self.knownMarkers = knownMarkers
        self.pos = [0, 0, 0]
        # self.rot = [0, 0, 0]
        self.running = True
        self.markers = {}  # tvec.  get from image processing
        self.knownMarkers = {}  # IDs of known markers
        # self.hoopMarkers = []  # these are the ids of the hoop markers

    def startOdometry(self):
        while(self.running == True):
            i = 1
            translation = [0, 0, 0]
            for item in self.markers.items():
                if item[0] in self.knownMarkers.keys():
                    translation = translation + \
                        (self.knownMarkers[item[0]] - item[1])
                    i = i + 1
                else:
                    self.knownMarkers[item[0]] = item[1] + self.pos
            translation = list(np.array(translation) / i)
            self.pos = translation

    def setMarkers(self, markers):  # markers is the output of cvloop.getOdoFormat()
        self.markers = {}
        for each in markers:
            self.markers[each[0]] = each[1] * np.array([1, -1, 1])

    def stopOdometry(self):
        self.running = False

    def getPos(self):
        return self.pos

    # def getRot(Self):
        # return self.rot
