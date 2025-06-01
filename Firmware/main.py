from helpers.stereocam import StereoVision
from helpers.obstacledetector import ObstacleDetector
from helpers.quadraped import QuadrupedWalker
import time

ik_params = {
    "link2_length": 5,
    "link3_length": 5,
    "y_rest": 4,
    "z_rest": 2,
    "leg_angle_offset": 20
}

leg_channels = {
    "front_left": [0, 1, 2],
    "front_right": [3, 4, 5],
    "back_left": [6, 7, 8],
    "back_right": [9, 10, 11]
}

vision = StereoVision()
detector = ObstacleDetector()
walker = QuadrupedWalker(ik_params, leg_channels)

print("Starting walk loop...")
while True:
    imgL, imgR = vision.capture_stereo_pair()
    disparity, depth = vision.compute_depth(imgL, imgR)

    if detector.detect_obstacle(depth):
        print("Obstacle detected!")
        walker.step_forward()
    else:
        walker.step_forward()

    time.sleep(0.5)
