import cv2
import threading
import time
from pathlib import Path

class WebcamRecorder:
    def __init__(self, output_file='data/webcam.mp4', fps=30, camera_index=0, memory_limit=100):
        self.output_file = output_file
        self.fps = fps
        self.recording = False
        self.frames = []
        self.memory_limit = memory_limit
        self.thread = None
        self.camera_index = camera_index

        # Open the webcam
        self.cap = cv2.VideoCapture(self.camera_index)
        # Timestamps of the frames
        csv_path = Path(self.output_file).with_suffix('.csv')
        self.csv_path = csv_path.parent / f'{csv_path.stem}_timestamps.csv'
        self.csv_path.write_text('frame_number,timestamp\n')

        # Check if the webcam is opened properly
        if not self.cap.isOpened():
            raise ValueError("Could not open video device")

        # Get the width and height of frames the camera is capturing
        # (TODO: Faulty code, always returns 640x480; so we should set them manually) # but because it always returns that res., I mean I trust it for some reason so I don't set it...(is this good behavior from me? maybe not.)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # Set auto focus to false
        self.cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)  # does this always set the same focus? if not, we might be in trouble I guess.
        # # more properties that might be useful being turned off instead (for calibration (intrinsics and extrinsics))
        # self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0) # exposure
        # self.cap.set(cv2.CAP_PROP_AUTO_WB, 0) # white balance
        # self.cap.set(cv2.CAP_PROP_BRIGHTNESS, 0) # brightness
        # self.cap.set(cv2.CAP_PROP_CONTRAST, 0) # contrast
        # self.cap.set(cv2.CAP_PROP_SATURATION, 0) # saturation
        # self.cap.set(cv2.CAP_PROP_HUE, 0) # hue
        # self.cap.set(cv2.CAP_PROP_GAIN, 0) # gain
        # self.cap.set(cv2.CAP_PROP_SHARPNESS, 0) # sharpness
        # self.cap.set(cv2.CAP_PROP_BACKLIGHT, 0) # backlight
        # self.cap.set(cv2.CAP_PROP_GAMMA, 0) # gamma

        # Just for face recognition - START
        if False:  # this should be false, right? jezus... xd what a shitty engineer I am.
            if camera_index == 0:
                self.width = 1280
                self.height = 720
            elif camera_index == 2:
                self.width = 1920
                self.height = 1080
        # Just for face recognition - END

        # Set properties
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

        # Define the codec and create a VideoWriter object
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = cv2.VideoWriter(self.output_file, self.fourcc, self.fps, (self.width, self.height))

    def start(self):
        self.recording = True
        self.thread = threading.Thread(target=self._record)
        self.thread.start()

    def stop(self):
        self.recording = False
        if self.thread is not None:
            self.thread.join()

        self.cap.release()
        self.out.release()

        self.thread = None

    def _record(self):
        # OpenCV with(!) FFMPEG installation to be able to use 'H264' codec instead of 'MP4V'
        self.out = cv2.VideoWriter(str(self.output_file), cv2.VideoWriter_fourcc(*'mp4v'), self.fps, (self.width, self.height))

        if not self.out.isOpened():
            print("Error: Video Writer could not be opened.")
            return

        frame_duration = 1 / self.fps
        start_time = time.time()
        frame_count = 0

        while self.recording:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Could not read frame from webcam.")
                break
            with self.csv_path.open('a') as f:
                f.write(f"{frame_count},{time.time()}\n")


            self.out.write(frame)
            self.frames.append(frame)
            self.frames = self.frames[-self.memory_limit:]

            print(f"Recording Frame: {frame_count}")

            frame_count += 1
            next_frame_time = start_time + frame_count * frame_duration
            sleep_time = next_frame_time - time.time()
