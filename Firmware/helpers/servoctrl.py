from adafruit_servokit import ServoKit
import time

class ServoController:
    def __init__(self, num_channels=16):
        self.kit = ServoKit(channels=num_channels)

    def set_angles(self, channel_angle_map):
        for channel, angle in channel_angle_map.items():
            angle = max(0, min(180, angle))
            self.kit.servo[channel].angle = angle

    def move_smoothly(self, current_angles, target_angles, channels, steps=10, delay=0.02):
        for step in range(steps + 1):
            interpolated = {
                ch: current_angles[ch] + (target_angles[ch] - current_angles[ch]) * (step / steps)
                for ch in channels
            }
            self.set_angles(interpolated)
            time.sleep(delay)
