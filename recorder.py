'''
A script that records and samples the inputs from the user
in order to be able to predict the user's next actions.
If done correctly, we can help the user to be understood by the computer easier and faster,
thus making the user's experience more enjoyable.
'''

# Imports
from recorders import MouseListener, AudioRecorder, ScreenRecorder




if __name__ == '__main__':
    mouse_listener = MouseListener(delta_time=0.03)
    mouse_listener.start()
    
    audio_recorder = AudioRecorder('data/audio.wav')
    audio_recorder.start()

    screen_recorder = ScreenRecorder(output_file='data/video.mp4', fps=30)
    screen_recorder.start()  # start recording

    while True:
        # mouse_events = mouse_listener.fetch_events()
        # if mouse_events:
        #     print('#Mouse events:', len(mouse_events))
        # audio_data = audio_recorder.fetch_audio_data()
        # if audio_data:
        #     print('Lenght of audio:', len(audio_data))
        import time
        time.sleep(3)
        print('Done')
        break
    print('Done23')
    
    # Stop recording
    screen_recorder.stop()
    audio_recorder.stop()
    mouse_listener.stop()