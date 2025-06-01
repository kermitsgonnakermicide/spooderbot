import numpy as np

class ObstacleDetector:
    def __init__(self, z_threshold=20, roi=(200, 400, 150, 330)):
        self.z_threshold = z_threshold  # mm
        self.roi = roi  # (x1, x2, y1, y2)

    def detect_obstacle(self, depth_map):
        x1, x2, y1, y2 = self.roi
        region = depth_map[y1:y2, x1:x2]
        z_values = region[:, :, 2]
        obstacle_mask = (z_values > 0) & (z_values < self.z_threshold)
        result = np.sum(obstacle_mask) > 300 
        return result