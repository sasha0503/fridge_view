import time

import cv2
from utils import get_stitched_images


class TestFrameCapture:

    def __init__(self):
        self.start_time = time.monotonic()
        self.cap_l = cv2.VideoCapture('data/videos/20_left_720.mp4')
        self.cap_r = cv2.VideoCapture('data/videos/20_right_720.mp4')
        self.fps_l = self.cap_l.get(cv2.CAP_PROP_FPS)
        self.fps_r = self.cap_r.get(cv2.CAP_PROP_FPS)

    def get_frame(self):
        time_elapsed = time.monotonic() - self.start_time
        frame_num_l = int(time_elapsed * self.fps_l)
        frame_num_r = int(time_elapsed * self.fps_r)
        self.cap_l.set(cv2.CAP_PROP_POS_FRAMES, frame_num_l)
        self.cap_r.set(cv2.CAP_PROP_POS_FRAMES, frame_num_r)
        return get_stitched_images(self.cap_r, self.cap_l, time_elapsed), time_elapsed
