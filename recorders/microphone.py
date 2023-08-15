"""
An AudioRecorder object is used to record audio from the system's default input audio device,
continuously writing the recorded data to a WAV file,
and also provide a fetch_audio_data function with which you can access
all the audio that is built up since the previous call to this function.

The class uses pyaudio to interface with the system's audio input and the wave module 
to write the audio data to a WAV file. It employs a separate thread to record audio 
while the rest of the program continues running.

Usage:
    recorder = AudioRecorder(output_file='data/audio.wav')
    recorder.start()  # start recording

    # do other stuff while recording...
    
    # fetch raw audio data (optional)
    raw_data = recorder.fetch_audio_data()  

    recorder.stop()  # stop recording

Parameters:
- output_file: path of the file where the recorded audio will be saved. 
    Default is 'data/audio.wav'.
- channels: number of audio channels to record. Default is 1 (mono).
- rate: sample rate in Hz. Default is 16000.
- chunk_size: size of audio chunks to read at a time. Default is 1024. Smaller values 
    may result in smoother audio, but too small values can cause performance issues.

Methods:
- start(): Start recording audio.
- stop(): Stop recording audio.
- fetch_audio_data(): Returns the raw audio data recorded since the last call to this method 
    and clears the internal buffer. This can be useful if you want to process the audio data 
    while you're recording. The data is returned as a bytes object.

Example:
    At the bottom of this file is a simple example of how to use this class.
"""

import atexit
import pyaudio
import threading
import wave
import time

from pathlib import Path


class MircophoneRecorder:
    def __init__(self, output_file='data/microphone.wav', channels=1, sample_rate=16000, chunk_size=1024, memory_limit=100):
        self.CHUNK = chunk_size
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = channels
        self.SAMPLERATE = sample_rate

        self.audio = pyaudio.PyAudio()
        self.stream = None

        self.frames = []
        self.memory_limit = memory_limit
        self.output_file = Path(output_file)
        self.wave_file = wave.open(output_file, 'wb')
        self.wave_file.setnchannels(self.CHANNELS)
        self.wave_file.setsampwidth(self.audio.get_sample_size(self.FORMAT))
        self.wave_file.setframerate(self.SAMPLERATE)
        atexit.register(self.stop)

        self.recording = False
        self.thread = None
        self.last_timestamp = time.time()

    def start(self):
        if self.stream is None:
            self.stream = self.audio.open(format=self.FORMAT,
                                          channels=self.CHANNELS,
                                          rate=self.SAMPLERATE,
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
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        self.wave_file.close
        self.audio.terminate()
        self.thread = None
        output_path = Path(self.output_file)
        output_path.with_name(output_path.stem + '_timestamp.txt').write_text(str(self.last_timestamp))

    def record(self):
        while self.recording:
            if self.stream is not None:
                data = self.stream.read(self.CHUNK)
                self.last_timestamp = time.time()
                self.frames.append(data)
                self.wave_file.writeframes(data)
                self.frames = self.frames[-self.memory_limit:]

    def fetch_audio_data(self):
        audio_data = b''.join(self.frames)
        self.frames = []
        return audio_data



if __name__ == '__main__':
    audio_recorder = MircophoneRecorder()
    audio_recorder.start()  # start recording

    # record for a while...
    import time
    time.sleep(5)

    # fetch audio data for processing
    data = audio_recorder.fetch_audio_data()
    print(len(data))

    # continue recording...
    time.sleep(3)

    # fetch more audio data for processing
    data = audio_recorder.fetch_audio_data()
    print(len(data))

    audio_recorder.stop()  # stop recording
