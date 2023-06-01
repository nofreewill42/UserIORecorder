import time
import atexit
import threading
import struct
from pynput.keyboard import Controller, Listener, Key

class KeyboardListener:
    def __init__(self, bin_file='data/keyboard_events.bin'):
        self.keyboard = Controller()
        self.start_time = time.time()

        self.bin_file = open(bin_file, 'wb', 0)
        atexit.register(self.bin_file.close)

        self.event2id = {'press':0,
                         'release':1}

        self.events = []
        self.lock = threading.Lock()

    def write_row(self, event_id, key, time):
        # key codes are generally up to 2 bytes in size
        binary_data = struct.pack('bid', event_id, key.value.vk, time)
        self.bin_file.write(binary_data)
        self.events.append(binary_data)

    def get_time(self):
        return time.time()

    def on_press(self, key):
        current_time = self.get_time()
        event_id = self.event2id['press']
        try:
            self.write_row(event_id, key, current_time)
        except AttributeError:
            pass  # Non-standard key pressed

    def on_release(self, key):
        current_time = self.get_time()
        event_id = self.event2id['release']
        try:
            self.write_row(event_id, key, current_time)
        except AttributeError:
            pass  # Non-standard key released

    def start(self):
        self.listener = Listener(on_press=self.on_press, on_release=self.on_release)
        self.thread = threading.Thread(target=self.listener.start)
        self.thread.start()

    def stop(self):
        print('Stopping keyboard listener...')
        if self.thread is not None:
            self.listener.stop()
            self.thread.join()
            print('Keyboard listener stopped.')
        else:
            print('Keyboard listener not running.')

    def fetch_events(self):
        with self.lock:
            events_data = b''.join(self.events)
            self.events = []
        return events_data
