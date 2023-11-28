import os

import cv2

"""
Cut the videos into frames for testing purposes.
"""


def cut_frames(video: cv2.VideoCapture, save_path: str, fps: int = 2):
    """
    Cut the given video into frames and save them to the given path.
    """
    if not video.isOpened():
        raise ValueError('video is not opened')

    # Get the frame count and fps of the video
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    video_fps = video.get(cv2.CAP_PROP_FPS)

    # Check if the fps is valid
    if fps <= 0 or fps > video_fps:
        raise ValueError('invalid fps')

    # Calculate the frame interval
    frame_interval = int(video_fps / fps)

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # Iterate through the frames and save them
    for i in range(0, frame_count, frame_interval):
        video.set(cv2.CAP_PROP_POS_FRAMES, i)
        _, frame = video.read()
        cv2.imwrite(save_path + f'frame_{i}.jpg', frame)


if __name__ == '__main__':
    video_r = cv2.VideoCapture('data/videos/20_right_720.mp4')
    cut_frames(video_r, 'data/frames/right/')

    video_l = cv2.VideoCapture('data/videos/20_left_720.mp4')
    cut_frames(video_l, 'data/frames/left/')

    video_c = cv2.VideoCapture('data/videos/20_center_1080.mp4')
    cut_frames(video_c, 'data/frames/center/')
