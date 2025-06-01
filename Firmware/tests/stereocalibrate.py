import cv2
import numpy as np
import glob

CHECKERBOARD = (9, 6)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objp = np.zeros((CHECKERBOARD[0]*CHECKERBOARD[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)

objpoints = []
imgpointsL = []
imgpointsR = []

images_left = sorted(glob.glob('left/*.jpg'))
images_right = sorted(glob.glob('right/*.jpg'))

for imgL_path, imgR_path in zip(images_left, images_right):
    imgL = cv2.imread(imgL_path)
    imgR = cv2.imread(imgR_path)
    grayL = cv2.cvtColor(imgL, cv2.COLOR_BGR2GRAY)
    grayR = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)

    retL, cornersL = cv2.findChessboardCorners(grayL, CHECKERBOARD, None)
    retR, cornersR = cv2.findChessboardCorners(grayR, CHECKERBOARD, None)

    if retL and retR:
        objpoints.append(objp)
        cornersL2 = cv2.cornerSubPix(grayL, cornersL, (11,11), (-1,-1), criteria)
        cornersR2 = cv2.cornerSubPix(grayR, cornersR, (11,11), (-1,-1), criteria)
        imgpointsL.append(cornersL2)
        imgpointsR.append(cornersR2)

retL, mtxL, distL, _, _ = cv2.calibrateCamera(objpoints, imgpointsL, grayL.shape[::-1], None, None)
retR, mtxR, distR, _, _ = cv2.calibrateCamera(objpoints, imgpointsR, grayR.shape[::-1], None, None)

# Stereo calibration
flags = cv2.CALIB_FIX_INTRINSIC
ret, _, _, _, _, R, T, E, F = cv2.stereoCalibrate(
    objpoints, imgpointsL, imgpointsR, mtxL, distL, mtxR, distR,
    grayL.shape[::-1], criteria=criteria, flags=flags)

# Stereo rectification
R1, R2, P1, P2, Q, roi1, roi2 = cv2.stereoRectify(
    mtxL, distL, mtxR, distR, grayL.shape[::-1], R, T, alpha=0)

np.savez('calib_data.npz', mtxL=mtxL, distL=distL, mtxR=mtxR, distR=distR, R=R, T=T, Q=Q)
