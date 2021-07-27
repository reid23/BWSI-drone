# this file has the odometry class
# it takes in the image from the drone and updates the position array


class odometry():
    pos = [0, 0, 0]
    rot = [0, 0, 0]
    running = True
    markers = {}  # id : [corner1, corner2, corner3, corner4]
    knownMarkers = {}

    def __init__(self, knownMarkers={}):
        self.knownMarkers = knownMarkers

    def startOdometry(self):
        while(self.running=True):
            for marker in markers:
                if marker in self.knownMarkers:
                    pass
                    # TODO get rvec, tvec, and use them to update self.pos and self.rot
                else:
                    pass
                    # TODO add point to path for path planner

    def stopOdometry(self):
        self.running = False
