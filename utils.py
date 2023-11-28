import cv2
import numpy as np


def get_stitched_images(video_r: cv2.VideoCapture, video_l: cv2.VideoCapture, timestamp: float) -> np.ndarray:
    """
    Take a given timestamp, extract a still frame at the given timestamp for each ultra-wide camera
    and stitch them together to form a single image.
    :param video_r: right ultra-wide camera video
    :param video_l: left ultra-wide camera video
    :param timestamp: timestamp to extract still frames from, measured in seconds
    :return: stitched image
    """
    # turn the timestamp into a frame number
    fps_r = video_r.get(cv2.CAP_PROP_FPS)
    fps_l = video_l.get(cv2.CAP_PROP_FPS)
    timestamp_frame_r = timestamp * fps_r
    timestamp_frame_l = timestamp * fps_l

    # Check if the timestamp is within the bounds of the video
    if timestamp_frame_r < 0 or timestamp_frame_r > video_r.get(cv2.CAP_PROP_FRAME_COUNT):
        raise ValueError('timestamp is out of bounds')
    if timestamp_frame_l < 0 or timestamp_frame_l > video_l.get(cv2.CAP_PROP_FRAME_COUNT):
        raise ValueError('timestamp is out of bounds')

    # Set the video capture to the given timestamp
    video_r.set(cv2.CAP_PROP_POS_FRAMES, timestamp_frame_r)
    video_l.set(cv2.CAP_PROP_POS_FRAMES, timestamp_frame_l)

    # Read the frame at the given timestamp
    _, frame_r = video_r.read()
    _, frame_l = video_l.read()

    # Stitch the frames together
    stitched_img = np.concatenate((frame_r, frame_l), axis=1)

    return stitched_img


if __name__ == '__main__':
    video_r = cv2.VideoCapture('data/videos/20_right_720.mp4')
    video_l = cv2.VideoCapture('data/videos/20_left_720.mp4')

    while True:
        timestamp_sec = input('Enter timestamp in seconds: ')
        if timestamp_sec == 'q':
            break
        try:
            image = get_stitched_images(video_r, video_l, float(timestamp_sec))

            cv2.namedWindow('image', cv2.WINDOW_NORMAL)
            cv2.imshow('image', image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        except ValueError as e:
            print(e)
