from InverseKinematics3D import InverseKinematics3D
from servoctrl import ServoController
import time

class QuadrupedWalker:
    def __init__(self, ik_params, leg_channels):
        self.ik = InverseKinematics3D(**ik_params)
        self.controller = ServoController()
        self.leg_channels = leg_channels
        self.leg_positions = {leg: (0, 0, -5) for leg in leg_channels}

    def move_leg(self, leg, xyz, steps=10):
        current = self.leg_positions[leg]
        for step in range(steps + 1):
            interp = [current[i] + (xyz[i] - current[i]) * (step / steps) for i in range(3)]
            angles = self.ik.calculate(*interp)
            self.controller.set_angles(dict(zip(self.leg_channels[leg], angles)))
            time.sleep(0.02)
        self.leg_positions[leg] = xyz

    def raise_leg_high(self, leg):
        x, y, z = self.leg_positions[leg]
        self.move_leg(leg, (x, y, z + 4))

    def sidestep(self, direction="left"):
        dx = 4 if direction == "right" else -4
        for leg in ["front_left", "back_left", "front_right", "back_right"]:
            x, y, z = self.leg_positions[leg]
            self.move_leg(leg, (x + dx, y, z))

    def step_forward(self):
        for leg in ["front_left", "back_right", "front_right", "back_left"]:
            x, y, z = self.leg_positions[leg]
            self.move_leg(leg, (x + 3, y, z))
