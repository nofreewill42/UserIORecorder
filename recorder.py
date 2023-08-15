'''
A script that records and samples the inputs from the user
in order to be able to predict the user's next actions.
If done correctly, we can help the user to be understood by the computer easier and faster,
thus making the user's experience more enjoyable.
'''

# Imports
import os
import time
from recorders import MouseListener, MircophoneRecorder, SpeakerRecorder, ScreenRecorder, KeyboardListener, WebcamRecorder

import signal
import sys
import time

import subprocess

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    # Call cleanup functions here
    # Stop recording
    screen_recorder.stop()
    webcam_recorder_0.stop()
    webcam_recorder_1.stop()
    microphone_recorder.stop()
    # speaker_recorder.stop()
    mouse_listener.stop()
    keyboard_listener.stop()
    #mouseview_recorder.stop()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


if __name__ == '__main__':
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    data_dir = f'data/{timestamp}'

    # Create a new directory for this interaction
    os.makedirs(data_dir, exist_ok=True)

    keyboard_listener = KeyboardListener(csv_file=f'{data_dir}/keyboard.csv')  # Add this line
    keyboard_listener.start()  # Start keyboard listener

    microphone_recorder = MircophoneRecorder(f'{data_dir}/microphone.wav')
    microphone_recorder.start()

    screen_recorder = ScreenRecorder(output_file=f'{data_dir}/screens.mp4', fps=4, downscale_factor=1, capture_radius=(5000,3000))
    screen_recorder.start()  # start recording

    fps = 15
    webcam_recorder_0 = WebcamRecorder(output_file=f'{data_dir}/webcam_0.mp4', camera_index=0, fps=fps)  # Add this line
    webcam_recorder_0.start()  # Start webcam recording
    webcam_recorder_1 = WebcamRecorder(output_file=f'{data_dir}/webcam_1.mp4', camera_index=2, fps=fps)  # Add this line
    webcam_recorder_1.start()  # Start webcam recording

    delta_time = None#0.03
    mouse_listener = MouseListener(delta_time=delta_time, bin_file=f'{data_dir}/mouse.bin')
    mouse_listener.start()

    # speaker_recorder = SpeakerRecorder(f'{data_dir}/speaker_audio.wav')
    # speaker_recorder.start()

    # mouseview_recorder = ScreenRecorder(output_file=f'{data_dir}/mouseview.mp4', fps=10, downscale_factor=2, capture_radius=(100,40))
    # mouseview_recorder.start()  # start recording

    while True:
        # mouse_events = mouse_listener.fetch_events()
        # if mouse_events:
        #     print('#Mouse events:', len(mouse_events))
        # audio_data = audio_recorder.fetch_audio_data()
        # if audio_data:
        #     print('Lenght of audio:', len(audio_data))
        # import time
        # time.sleep(30)
        # break
        time.sleep(0.1)
        pass
    
    # Stop recording
    screen_recorder.stop()
    webcam_recorder_0.stop()
    webcam_recorder_1.stop()
    microphone_recorder.stop()
    mouse_listener.stop()
    keyboard_listener.stop()
    # speaker_recorder.stop()
    #mouseview_recorder.stop()
