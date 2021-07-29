# this file has the odometry class
# it takes in the image from the drone and updates the position array


class odometry():
    def __init__(self, knownMarkers={}):
        self.knownMarkers = knownMarkers
        self.pos = [0, 0, 0]
        self.rot = [0, 0, 0]
        self.running = True
        self.ids
        self.markers = []  # tvec.  get from image processing
        self.knownMarkers = []  # IDs of known markers
        self.hoopMarkers = []  # these are the ids of the hoop markers

    def startOdometry(self):
        while(self.running == True):
            for marker in self.markers:
                if marker in self.knownMarkers:
                    pass
                    # TODO get rvec, tvec, and use them to update self.pos and self.rot
                elif marker in self.hoopMarkers:
                    pass
                else:
                    self.hoopMarkers[marker] = self.markers[marker]

    def hoopPoses(self):
        pass
        # return hoop positions

    def setMarkers(self, markers):
        self.markers = markers

    def stopOdometry(self):
        self.running = False

    def getPos(self):
        return self.pos

    def getRot(Self):
        return self.rot
