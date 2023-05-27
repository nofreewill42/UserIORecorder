'''
A script that records and samples the inputs from the user
in order to be able to predict the user's next actions.
If done correctly, we can help the user to be understood by the computer much faster.
'''

# Imports
from recorders import MouseListener, AudioRecorder




if __name__ == '__main__':
    ml = MouseListener(delta_time=0.03)
    ml.start()
    
    recorder = AudioRecorder()
    recorder.start()

    while True:
        pass