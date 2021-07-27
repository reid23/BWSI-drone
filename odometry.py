# this file has the odometry class
# it takes in the image from the drone and updates the position array


class odometry():
    pos = [0, 0, 0]
    rot = [0, 0, 0]
    running = True
    def __init__(self, knownMarkers={}):

    def startOdometry(self):
        while(self.running=True):
            pass

    def stopOdometry(self):
        self.running = False
