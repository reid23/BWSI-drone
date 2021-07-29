# this file has the odometry class
# it takes in the image from the drone and updates the position array


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
        self.rot = [0, 0, 0]
        self.hoopPosList = []
        self.running = True
        self.knownMarkersIds = []  # IDs of known markers
        self.hoopMarkersIds = []  # these are the ids of the hoop markers

    def startOdometry(self):
        while(self.running == True):
            for marker in self.markersDictFixed:
                if marker in self.knownMarkers:
                    pass
                    # TODO get rvec, tvec, and use them to update self.pos and self.rot
                elif marker in self.hoopMarkers:
                    # TODO: calculate the global position of the marker and append that
                    self.hoopPosList = self.hoopPoses()
                else:
                    self.hoopMarkers.append(marker)

    def hoopPoses(self):

        # return hoop positions

    def setMarkers(self, markers):  # markers is the output of cvloop.getOdoFormat()
        d = Dictlist()
        for i in range(len(markers[0])):
            d[markers[0][i]] = markers[1][i]
        self.markersDictFixed = d
        self.markers = markers[1]
        self.ids = markers[0]

    def stopOdometry(self):
        self.running = False

    def getPos(self):
        return self.pos

    def getRot(Self):
        return self.rot
