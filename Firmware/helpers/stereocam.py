import cv2
import numpy as np
import time
from picamera.array import PiRGBArray
from picamera import PiCamera

class StereoVision:
    def __init__(self, calib_path='calib_data.npz'):
        self.calib = np.load(calib_path)
        self.stereo = cv2.StereoSGBM_create(
            numDisparities=64,
            blockSize=5,
            minDisparity=0,
            uniquenessRatio=10,
            speckleWindowSize=100,
            speckleRange=32,
            disp12MaxDiff=1,
            P1=8*3*5**2,
            P2=32*3*5**2
        )

    def capture_stereo_pair(self):
            cam1 = PiCamera(camera_num=0, resolution=(640, 480))
            cam2 = PiCamera(camera_num=1, resolution=(640, 480)) 

            raw1 = PiRGBArray(cam1)
            raw2 = PiRGBArray(cam2)
            time.sleep(2)

            cam1.capture(raw1, format="bgr")
            cam2.capture(raw2, format="bgr")

            return raw1.array, raw2.array

    def compute_depth(self, imgL, imgR):
        mtxL, distL = self.calib['mtxL'], self.calib['distL']
        mtxR, distR = self.calib['mtxR'], self.calib['distR']
        R, T, Q = self.calib['R'], self.calib['T'], self.calib['Q']

        h, w = imgL.shape[:2]
        R1, R2, P1, P2, Q, _, _ = cv2.stereoRectify(mtxL, distL, mtxR, distR, (w, h), R, T)
        map1x, map1y = cv2.initUndistortRectifyMap(mtxL, distL, R1, P1, (w, h), cv2.CV_32FC1)
        map2x, map2y = cv2.initUndistortRectifyMap(mtxR, distR, R2, P2, (w, h), cv2.CV_32FC1)

        rectL = cv2.remap(imgL, map1x, map1y, cv2.INTER_LINEAR)
        rectR = cv2.remap(imgR, map2x, map2y, cv2.INTER_LINEAR)

        disparity = self.stereo.compute(
            cv2.cvtColor(rectL, cv2.COLOR_BGR2GRAY),
            cv2.cvtColor(rectR, cv2.COLOR_BGR2GRAY)
        ).astype(np.float32) / 16.0

        depth = cv2.reprojectImageTo3D(disparity, Q)
        return disparity, depth
