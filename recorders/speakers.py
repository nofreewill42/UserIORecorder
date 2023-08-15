import atexit
import pyaudio
import threading
import wave

from pathlib import Path

class SpeakerRecorder:
    def __init__(self, output_file='data/speaker.wav', channels=1, sample_rate=44100, chunk_size=1024, memory_limit=100):
        self.CHUNK = chunk_size
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = channels
        self.RATE = sample_rate
        self.output_file = str(Path(output_file).absolute())
        self.frames = []
        self.memory_limit = memory_limit
        self.recording = False
        self.audio = pyaudio.PyAudio()
        self.stream = None

        self.device_name = "pulse"

        self.wave_file = wave.open(self.output_file, 'wb')
        self.wave_file.setnchannels(self.CHANNELS)
        self.wave_file.setsampwidth(self.audio.get_sample_size(self.FORMAT))
        self.wave_file.setframerate(self.RATE)
        atexit.register(self.stop)

    def get_device_index(self, device_name):
        for i in range(self.audio.get_device_count()):
            device_info = self.audio.get_device_info_by_index(i)
            if device_info["name"] == device_name:
                return i
        raise ValueError(f"No device with name {device_name} found")

    def start(self):
        self.recording = True
        device_index = self.get_device_index(self.device_name)

        self.stream = self.audio.open(format=self.FORMAT,
                                    channels=self.CHANNELS,
                                    rate=self.RATE,
                                    input=True,
                                    frames_per_buffer=self.CHUNK,
                                    input_device_index=device_index)
        self.thread = threading.Thread(target=self.record)
        self.thread.start()

    def stop(self):
        self.recording = False
        if self.thread is not None:
            self.thread.join()  # Wait for recording thread to finish
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        self.wave_file.close()
        self.audio.terminate()
        self.thread = None

    def record(self):
        while self.recording:
            if self.stream is not None:
                data = self.stream.read(self.CHUNK)
                self.frames.append(data)
                self.wave_file.writeframes(data)
                self.frames = self.frames[-self.memory_limit:]

    def fetch_audio_data(self):
        audio_data = b''.join(self.frames)
        self.frames = []
        return audio_data

if __name__ == '__main__':
    speaker_recorder = SpeakerRecorder()
    speaker_recorder.start()  # start recording

    # record for a while...
    import time
    time.sleep(5)

    # fetch audio data for processing
    data = speaker_recorder.fetch_audio_data()
    print(len(data))

    # continue recording...
    time.sleep(3)

    # fetch more audio data for processing
    data = speaker_recorder.fetch_audio_data()
    print(len(data))

    speaker_recorder.stop()  # stop recording
