import os

import cv2

from rack_detection import RackDetector
from streaming_utils import TestFrameCapture

FPS = 10
frame_capture = TestFrameCapture()
rack_detector = RackDetector(detection_interval=1)
res_folder = 'data/rack_detection/'
os.makedirs(res_folder, exist_ok=True)
cv2.namedWindow('frame', cv2.WINDOW_NORMAL)

while True:
    frame, timestamp = frame_capture.get_frame()
    if frame is None:
        break
    res_img = rack_detector.detect(frame)
    if res_img is not None:
        print('########### Rack detected, dumping image')
        cv2.imwrite(os.path.join(res_folder, f'{timestamp}.jpg'), res_img)

    cv2.imshow('frame', frame)
    cv2.waitKey(int(1000 / FPS))
