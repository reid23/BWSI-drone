from djitellopy import Tello
import numpy as np
import cv2


# important variables for video loop
cameraMatrix = np.array([[921.170702, 0.000000, 459.904354], [
                        0.000000, 919.018377, 351.238301], [0.000000, 0.000000, 1.000000]])
distortion = np.array([-0.033458, 0.105152, 0.001256, -0.006647, 0.000000])


class cvLoop:
    def __init__(self):
        #self.rvec = {}
        self.tvecIds = []
        self.tvecValues = []

    cameraMatrix = np.array([[921.170702, 0.000000, 459.904354], [
        0.000000, 919.018377, 351.238301], [0.000000, 0.000000, 1.000000]])
    distortion = np.array([-0.033458, 0.105152, 0.001256, -0.006647, 0.000000])

    def odoFormat(self):
        output = []
        for i in range(len(self.tvecIds)):
            output.append([self.tvecIds[i], self.tvecValues[i]])
        return output

    def imageProcessing(self, tello):
        # Video Loop:
        while True:
            img = tello.get_frame_read().frame
            dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_250)
            params = cv2.aruco.DetectorParameters_create()
            corners, ids, _ = cv2.aruco.detectMarkers(
                img, dict, parameters=params)  # finding aruco markers
            if corners:  # aruco loop
                checked_ids = []  # recording used ids, only performs calculations once per every two markers
                tvecIds = []
                tvecValues = []
                for i in range(len(corners)):
                    if ids[i] in checked_ids:
                        continue  # checks if it's been reviewed yet
                    # marks that it is now being reviews
                    checked_ids.append(ids[i])
                    try:  # finding index of other marker in list of arucos
                        o = ids.flatten().tolist().index(ids[i], i + 1)
                        other = corners[o]
                    except:
                        continue  # skipping this loop entirely if it's not found
                    pts = corners[i][0]
                    pts = pts.reshape((-1, 1, 2))
                    # drawing square around arucos
                    cv2.polylines(img, np.int32([pts]), True, (255, 0, 0), 5)
                    cv2.polylines(img, np.int32(
                        [other[0]]), True, (255, 0, 0), 5)
                    # drawing dots on top left corner of arucos
                    cv2.circle(img, (int(pts[0][0][0]), int(
                        pts[0][0][1])), 5, (0, 0, 255), -1)
                    cv2.circle(img, (int(other[0][0][0]), int(
                        other[0][0][1])), 5, (0, 0, 255), -1)
                    rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(
                        corners[i], 50, cameraMatrix, distortion)  # finding rvecs and tvecs for both markers
                    rvecs2, tvecs2, _ = cv2.aruco.estimatePoseSingleMarkers(
                        other, 50, cameraMatrix, distortion)
                    # averaging them
                    rvec = np.mean(np.array([rvecs, rvecs2]), axis=0)
                    tvec = np.mean(np.array([tvecs, tvecs2]), axis=0)
                    # checking that rvec is accurate (there were some problems with inaccuracies
                    try:
                        if abs(lastrvec[0][0][0] - rvec[0][0][0]) > 0.5:
                            rvec = lastrvec
                        else:
                            lastrvec = rvec
                    except:
                        lastrvec = rvec
                    # drawing marker
                    cv2.aruco.drawAxis(img, cameraMatrix,
                                       distortion, rvec, tvec, 30)
                    tvecIds.append(ids[i][0])
                    tvecValues.append(tvec[0][0])
                self.tvecIds = tvecIds
                self.tvecValues = tvecValues

            # Displaying screen
            battery = "Battery: " + str(tello.get_battery()) + "%"
            cv2.putText(img, battery, (650, 30),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            minutes, seconds = divmod(tello.get_flight_time(), 60)
            flight = "Flight Time: " + str(minutes) + ":" + str(seconds)
            cv2.putText(img, flight, (650, 60),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            barometer = "Altitude: " + \
                "{:.1f}".format(tello.get_height() / 100) + "m"
            cv2.putText(img, barometer, (650, 90),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow("Image", img)
            cv2.waitKey(5)
