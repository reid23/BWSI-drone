# this file has the odometry class
# it takes in the image from the drone and updates the position array


class odometry():
    def __init__(self, knownMarkers={}):
        self.knownMarkers = knownMarkers
        self.pos = [0, 0, 0]
        self.rot = [0, 0, 0]
        self.running = True
        self.markers = {}  # id : [rvec, tvec].  get from image processing
        self.knownMarkers = {}
        self.hoopMarkers = {}  # these are the unkown markers.  for path-following

    def startOdometry(self):
        while(self.running == True):
            for marker in self.markers:
                if marker in self.knownMarkers:
                    pass
                    # TODO get rvec, tvec, and use them to update self.pos and self.rot
                else:
                    pass
                    # TODO add point to path for path planner

    def setMarkers(self, markers):
        self.markers = markers

    def stopOdometry(self):
        self.running = False

    def getPos(self):
        return self.pos

    def getRot(Self):
        return self.rot
