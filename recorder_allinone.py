'''
A script that records and samples the inputs from the user
in order to be able to predict the user's next actions.
If done correctly, we can help the user to be understood by the computer easier and faster,
thus making the user's experience more enjoyable.
'''

# Imports
import os
import time
import numpy as np
from recorders import MouseListener, MircophoneRecorder, SpeakerRecorder, ScreenRecorder, KeyboardListener, WebcamRecorder

import signal
import sys
import time
import socketio

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


def create_socket_io(url, handle):
    sio = socketio.Client()
    try:
        sio.connect(url)
        sio.on('audio_results', handle)
        return sio
    except Exception as e:
        print(f'Error connecting to {url}: {e}')
        return None


def handle_audio_results(data):
    # Process the results received from the server
    print("Received audio results:", np.array(data).shape)



if __name__ == '__main__':
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    data_dir = f'data/{timestamp}'
    # Assistant - START
    conversational_training_data_dir = f'conversational_training_data'
    conversational_training_data_text_path = f'{conversational_training_data_dir}/{timestamp}.txt'
    os.makedirs(conversational_training_data_dir, exist_ok=True)
    conversational_training_data_file = open(conversational_training_data_text_path, "w", buffering=1)
    # Assistant - END

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

    # Assistant - START
    from whisper_streaming.whisper_online import *
    asr = FasterWhisperASR("en", "large-v2")
    online = OnlineASRProcessor(asr)
    # import ollama
    # messages = []
    import requests
    import time
    jetson_nano_url = 'http://192.168.0.24:5000'  # Replace with the actual IP address
    user_text = ''
    lamp_state = 'off'
    def control_lamp(signal, verbose=False):
        global lamp_state
        response = requests.post(f'{jetson_nano_url}/control', json={'signal': signal})
        lamp_state = signal
        if verbose: print(response.text)
    # Assistant - END

    while True:
        time.sleep(0.2)

        # Fetch raw audio data
        raw_audio = microphone_recorder.fetch_audio_data()
        audio_np = np.frombuffer(raw_audio, dtype=np.int16)
        if raw_audio:
            online.insert_audio_chunk(audio_np)
            _,_,o = online.process_iter()
            if len(o) > 0:
                current_user_text = "User: " + o
                user_text = user_text + o
                print(current_user_text)
                print(current_user_text, file=conversational_training_data_file, flush=False)
                #print(user_text)
                # Ollama - START
                if user_text.lower().replace('.', '').replace('?', '').replace('!', '').endswith('turn it on'):
                    control_lamp('on', verbose=True)
                elif user_text.lower().replace('.', '').replace('?', '').replace('!', '').endswith('turn it off'):
                    control_lamp('off', verbose=True)
                response = 'Assistant: ' + ''
                print(response)
                print(response, file=conversational_training_data_file, flush=False)
                # Ollama - END

            #     # send to ollama and receive results - START [TOBELABELLED]
            #     response = ollama.chat(model='mistral', messages=messages)
            #     response_text = response['message']['content']
            #     # send to ollama and receive results - END
            #     # make example of running all this and having the ASR results and label them with what we want mistral to say to each request. - START

            #     # make example of running all this and having the ASR results and label them with what we want mistral to say to each request. - END
                # Ollama - END
    
    # Stop recording
    screen_recorder.stop()
    webcam_recorder_0.stop()
    webcam_recorder_1.stop()
    microphone_recorder.stop()
    mouse_listener.stop()
    keyboard_listener.stop()
    # speaker_recorder.stop()
    #mouseview_recorder.stop()

    sio.disconnect()