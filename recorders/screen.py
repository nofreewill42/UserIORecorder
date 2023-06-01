"""
A ScreenRecorder Object is a class that can be used to record the screen continuously to a video file.
The recording if chosen will only include frames where the screen content changes (in a structural similarity more than a certain threshold).

It uses the opencv-python module to capture the screen and the ffmpeg-python module to encode the video.

Usage:
    To record the screen continuously to a video file:
    recorder = ScreenRecorder(output_file='data/video.mp4', fps=30)
    recorder.start()  # start recording

    # do other stuff while recording...

    recorder.stop()  # stop recording

Parameters:
- output_file: path of the file where the recorded video will be saved. Default is 'data/video.mp4'.
- fps: frames per second. Default is 30.

Methods:
- start(): Start recording the screen.
- stop(): Stop recording the screen.
- fetch_frames(): Return all the frames that were captured since the previous call to this method.

Example:
    At the bottom of this file is a simple example of how to use this class.
"""

# Imports
import numpy as np
import threading
import time
import cv2
from skimage.metrics import structural_similarity as ssim
from pathlib import Path
import pyautogui

import mss
import mss.tools





class ScreenRecorder:
    def __init__(self, output_file='data/video.mp4', fps=30, downscale_factor=1):
        self.output_file = Path(output_file)
        self.fps = fps
        self.recording = False
        self.frames = []  # Queue for video frames
        self.thread = None
        self.last_frame = None
        self.downscale_factor = downscale_factor  # Downscale the image to reduce the size of the video

    def start(self):
        if self.recording:
            return
        self.recording = True
        self.thread = threading.Thread(target=self._record)
        self.thread.start()

    def stop(self):
        if not self.recording:
            return
        self.recording = False
        self.thread.join()
        self.out.release()
        self.thread = None

    def fetch_frames(self):
        # Get the current list of frames and clear the list
        frames = self.frames
        self.frames = []
        return frames
    
    def _record(self):
        # TODO: OpenCV with(!) FFMPEG installation to be able to use 'H264' codec isntead of 'MP4V'
        screen_width, screen_height = pyautogui.size()
        self.out = cv2.VideoWriter(str(self.output_file), cv2.VideoWriter_fourcc(*'mp4v'), self.fps, (screen_width//self.downscale_factor, screen_height//self.downscale_factor))
        frame_duration = 1 / self.fps
        start_time = time.time()
        frame_count = 0

        while self.recording:
            #img = pyautogui.screenshot()
            

            with mss.mss() as sct:
                # The screen part to capture
                region = {'top': 0, 'left': 0, 'width': screen_width, 'height': screen_height}

                # Grab the data
                img = sct.grab(region)

                # # Save to the picture file
                # mss.tools.to_png(img.rgb, img.size, output='dummy.png')


            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert the image from BGR color space to RGB color space
            frame = cv2.resize(frame, (screen_width//self.downscale_factor, screen_height//self.downscale_factor))  # Downscale the image to reduce the size of the video
            if self.last_frame is not None:
                #score, diff = ssim(self.last_frame, frame, full=True, multichannel=True, channel_axis=2)
                if True:#score < 0.50:  # 0.99 was by default  # Threshold for similarity
                    self.out.write(frame)
                    self.frames.append(frame)
                else:
                    out.write(self.last_frame)
                    #self.frames.append(self.last_frame)
            else:
                self.out.write(frame)
                self.frames.append(frame)
            self.last_frame = frame

            frame_count += 1
            next_frame_time = start_time + frame_count * frame_duration
            sleep_time = next_frame_time - time.time()
            if sleep_time > 0:
                time.sleep(sleep_time)  # Sleep to limit the frame rate up to fps

        self.out.release()

if __name__ == '__main__':
    screen_recorder = ScreenRecorder(output_file='data/video.mp4', fps=30)
    screen_recorder.start()  # start recording

    # record for a while...
    import time
    time.sleep(5)

    # fetch recorded frames for processing
    frames = screen_recorder.fetch_frames()
    print(len(frames))

    # continue recording...
    time.sleep(3)

    # fetch more recorded frames for processing
    frames = screen_recorder.fetch_frames()
    print(len(frames))

    screen_recorder.stop()  # stop recording