import time
import atexit
import threading
import csv
import pyxhook

class KeyboardListener:
    def __init__(self, csv_file='data/keyboard_events.csv'):
        self.keyboard = pyxhook.HookManager()
        self.start_time = time.time()

        self.csv_file = open(csv_file, 'w', newline='', buffering=1)
        self.writer = csv.writer(self.csv_file)
        self.writer.writerow(['event', 'key', 'time'])  # write header
        atexit.register(self.csv_file.close)

        self.events = []
        self.lock = threading.Lock()
        self.pressed_keys = set()

    def write_row(self, event, key_name, time):
        row = [event, key_name, time]
        self.writer.writerow(row)
        self.events.append(row)

    def get_time(self):
        return time.time()

    def on_press(self, event):
        current_time = self.get_time()
        if event.Key in self.pressed_keys:
            return
        self.pressed_keys.add(event.Key)
        self.write_row(0, event.Key, current_time)

    def on_release(self, event):
        current_time = self.get_time()
        self.pressed_keys.discard(event.Key)
        self.write_row(1, event.Key, current_time)

    def start(self):
        self.keyboard.KeyDown = self.on_press
        self.keyboard.KeyUp = self.on_release
        self.thread = threading.Thread(target=self.keyboard.start)
        self.thread.start()

    def stop(self):
        print('Stopping keyboard listener...')
        if self.thread is not None:
            self.keyboard.cancel()
            self.thread.join()
            print('Keyboard listener stopped.')
        else:
            print('Keyboard listener not running.')

    def fetch_events(self):
        with self.lock:
            events_copy = self.events.copy()
            self.events.clear()
        return events_copy
