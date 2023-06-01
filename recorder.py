'''
A script that records and samples the inputs from the user
in order to be able to predict the user's next actions.
If done correctly, we can help the user to be understood by the computer easier and faster,
thus making the user's experience more enjoyable.
'''

# Imports
import os
import time
from recorders import MouseListener, AudioRecorder, ScreenRecorder, KeyboardListener

import signal
import sys
import time

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    # Call cleanup functions here
    # Stop recording
    mouseview_recorder.stop()
    screen_recorder.stop()
    audio_recorder.stop()
    mouse_listener.stop()
    keyboard_listener.stop()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


if __name__ == '__main__':
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    data_dir = f'data/{timestamp}'

    # Create a new directory for this interaction
    os.makedirs(data_dir, exist_ok=True)

    mouse_listener = MouseListener(delta_time=0.03, bin_file=f'{data_dir}/mouse_events.bin')
    mouse_listener.start()

    keyboard_listener = KeyboardListener(csv_file=f'{data_dir}/keyboard_events.csv')  # Add this line
    keyboard_listener.start()  # Start keyboard listener

    audio_recorder = AudioRecorder(f'{data_dir}/audio.wav')
    audio_recorder.start()

    screen_recorder = ScreenRecorder(output_file=f'{data_dir}/screens.mp4', fps=4, downscale_factor=4, capture_radius=(5000,3000))
    screen_recorder.start()  # start recording

    mouseview_recorder = ScreenRecorder(output_file=f'{data_dir}/mouseview.mp4', fps=10, downscale_factor=2, capture_radius=(100,40))
    mouseview_recorder.start()  # start recording

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
        pass
    
    # Stop recording
    mouseview_recorder.stop()
    screen_recorder.stop()
    audio_recorder.stop()
    mouse_listener.stop()
    keyboard_listener.stop()