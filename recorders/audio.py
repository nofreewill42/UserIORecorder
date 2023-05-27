import atexit
import pyaudio
import threading

from pathlib import Path


class AudioRecorder:
    def __init__(self, output_file='data/audio.aac', channels=1, rate=44100, chunk_size=1024):
        self.CHUNK = chunk_size
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = channels
        self.RATE = rate

        self.audio = pyaudio.PyAudio()
        self.stream = None

        self.frames = []
        self.output_file = Path(output_file)
        self.temp_file = self.output_file.with_suffix('.wav')
        self.bin_file = self.temp_file.open('wb')
        atexit.register(self.bin_file.close)

        self.recording = False
        self.thread = None

    def start(self):
        if self.stream is None:
            self.stream = self.audio.open(format=self.FORMAT,
                                          channels=self.CHANNELS,
                                          rate=self.RATE,
                                          input=True,
                                          frames_per_buffer=self.CHUNK)
        self.stream.start_stream()
        self.recording = True

        self.thread = threading.Thread(target=self.record)
        self.thread.start()

    def stop(self):
        self.recording = False
        if self.thread is not None:
            self.thread.join()  # Wait for recording thread to finish
        self.stream.stop_stream()
        self.stream.close()

    def record(self):
        while self.recording:
            data = self.stream.read(self.CHUNK)
            self.frames.append(data)
            self.bin_file.write(data)

    def fetch_audio_data(self):
        audio_data = b''.join(self.frames)
        self.frames = []
        return audio_data

    def __del__(self):
        self.stop()
        self.audio.terminate()




recorder = AudioRecorder()
recorder.start()  # start recording


# record for a while...
import time
time.sleep(5)

# fetch audio data
data = recorder.fetch_audio_data()

# continue recording...
time.sleep(15)

# fetch more audio data
more_data = recorder.fetch_audio_data()

recorder.stop()  # stop recording
