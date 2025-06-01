import math
import time

class InverseKinematics3D:
    def __init__(self, link2_length, link3_length, y_rest, z_rest, leg_angle_offset):
        self.j2_length = link2_length
        self.j3_length = link3_length
        self.y_rest = y_rest
        self.z_rest = z_rest
        self.leg_angle_offset = leg_angle_offset

    def clamp(self, v):
        return max(min(v, 1.0), -1.0)

    def calculate(self, x, y, z):
        y += self.y_rest
        z += self.z_rest

        j1 = math.degrees(math.atan2(x, y))
        h = math.hypot(x, y)
        l = math.hypot(h, z)

        max_reach = self.j2_length + self.j3_length
        min_reach = abs(self.j2_length - self.j3_length)
        if not (min_reach <= l <= max_reach):
            raise ValueError("yeh number network coverage shetra ke bahar hai")

        cos_j3 = self.clamp((self.j2_length**2 + self.j3_length**2 - l**2) / (2 * self.j2_length * self.j3_length))
        j3 = math.degrees(math.acos(cos_j3))

        cos_b = self.clamp((l**2 + self.j2_length**2 - self.j3_length**2) / (2 * l * self.j2_length))
        b = math.degrees(math.acos(cos_b))

        a = math.degrees(math.atan2(z, h))
        j2 = b + a

        servo_j1 = 90 - j1
        servo_j2 = 90 - j2
        servo_j3 = j3 + self.leg_angle_offset - 90

        return servo_j1, servo_j2, servo_j3

    def interpolate(self, start, end, steps):
        return [(start[i] + (end[i] - start[i]) * (step / steps)) for step in range(steps + 1) for i in range(3)]
