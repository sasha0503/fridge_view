import time

import cv2


class RackDetector:
    def __init__(self, set_size=5, detection_interval=1):
        self.detection_interval = detection_interval
        self.last_timestamp = 0
        self.central_idx = set_size // 2
        self.set_size = set_size
        self.contours_len = [0] * set_size
        self.images = [None] * set_size
        self.timestamps = [0] * set_size

    @staticmethod
    def get_contours_len(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200, apertureSize=3)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return len(contours)

    def detect(self, image):
        time_now = time.monotonic()
        if time_now - self.last_timestamp < self.detection_interval:
            return None
        self.last_timestamp = time_now
        current_len_contours = self.get_contours_len(image)

        self.contours_len.append(current_len_contours)
        self.images.append(image)
        if len(self.contours_len) > self.set_size:
            self.contours_len.pop(0)
            self.images.pop(0)
        else:
            return None

        central_len = self.contours_len[self.central_idx]
        set_compare = self.contours_len[:self.central_idx] + self.contours_len[self.central_idx + 1:]

        if all((central_len - len_contours) > 0 for len_contours in set_compare):
            return self.images[self.central_idx]
