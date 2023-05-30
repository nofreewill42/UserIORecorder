"""
A MouseListener object is used to monitor mouse events, including movements, clicks and scroll events.
These events are continuously written to a binary file.
The class also provides a fetch_events method which can be used to
access all the mouse event data that has been accumulated since the previous call to this function.

The class uses pynput.mouse to interface with the system's mouse
and the built-in struct module to encode the mouse event data as binary.

Usage:
    listener = MouseListener(delta_time=0.03)
    listener.start()  # start listening to mouse events

    # do other stuff while listening to mouse events...
    
    # fetch raw mouse event data (optional)
    raw_data = listener.fetch_events()

    listener.stop()  # stop listening

Parameters:
- delta_time: Minimum time in seconds between two consecutive mouse movement events.
    Default is None, meaning that every single movement event will be recorded.

Methods:
- start(): Start listening to mouse events.
- stop(): Stop listening to mouse events.
- fetch_events(): Returns the raw mouse event data recorded since the last call to this method and clears the internal buffer.
    This can be useful if you want to process the mouse event data while you're still recording. The data is returned as a bytes object.

Mouse events are recorded as follows:
- Event ID (1 byte):
    0 for movement,
    1 for left button press, 2 for left button release, 3 for right button press, 4 for right button release,
    5 for scroll event.
- x and y (2 bytes each): The x and y coordinates of the mouse pointer for movement and click events.
    For scroll events, these are the x and y distances scrolled.
- time (8 bytes): The time at which the event occurred, as returned by time.time().

Example:
    At the bottom of this file is a simple example of how to use this class.
"""


import atexit
import struct
import time
import threading
from pynput.mouse import Controller, Listener


class MouseListener:
    def __init__(self, delta_time=None):
        self.mouse = Controller()
        self.prev_position = self.mouse.position
        self.delta_time = delta_time
        self.start_time = time.time()
        self.prev_time = self.start_time  # used to check if the mouse has moved more than delta_time

        self.bin_file = open('data/mouse_events.bin', 'wb', 0)
        atexit.register(self.bin_file.close)  # make sure the file is being closed when the program exits

        self.event2id = {'move':0,
                         'click_left_press':1,
                         'click_left_release':2,
                         'click_right_press':3,
                         'click_right_release':4,
                         'scroll':5}

        self.events = []  # store the events
        self.lock = threading.Lock()  # for thread-safe operations

    def write_row(self, event_id, x, y, time):
        binary_data = struct.pack('bhhd', event_id, x, y, time)  # b: byte, h: short, d: double; for unsigned use B, H
        self.bin_file.write(binary_data)
        self.events.append(binary_data)

    def get_time(self):
        return time.time() # - self.start_time

    def on_move(self, x, y):
        current_time = self.get_time()

        # only record if the mouse has moved more than delta_time
        if self.delta_time is not None:
            if (current_time - self.prev_time) < self.delta_time:
                return
            self.prev_time = current_time
        
        current_position = (x, y)
        if self.prev_position != current_position:
            self.prev_position = current_position
            event_id = self.event2id['move']
            self.write_row(event_id, x, y, current_time)

    def on_click(self, x, y, button, pressed):
        current_time = self.get_time()
        event_id = -1  # default value : unknown event
        if button == button.left:
            if pressed:
                event_id = self.event2id['click_left_press']
            else:
                event_id = self.event2id['click_left_release']
        elif button == button.right:
            if pressed:
                event_id = self.event2id['click_right_press']
            else:
                event_id = self.event2id['click_right_release']
        self.write_row(event_id, x, y, current_time)

    def on_scroll(self, x, y, dx, dy):
        current_time = self.get_time()
        event_id = self.event2id['scroll']
        self.write_row(event_id, dx, dy, current_time)

    def start(self):
        self.thread = threading.Thread(target=self._start_listening)
        self.thread.start()

    def _start_listening(self):
        with Listener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll) as listener:
            listener.join()
    
    def stop(self):
        print('Stopping mouse listener...')
        if self.thread is not None:
            self.thread.join()  # Wait for listener thread to finish
            print('Mouse listener stopped.')
        else:
            print('Mouse listener not running.')
    
    def fetch_events(self):
        with self.lock:
            events_data = b''.join(self.events)
            self.events = []
        return events_data


if __name__ == '__main__':
    mouse_listener = MouseListener(delta_time=0.1)
    mouse_listener.start()  # start listening

    # listen for a while...
    import time
    time.sleep(5)

    # fetch mouse event data for processing
    data = mouse_listener.fetch_events()
    print(len(data))

    # continue listening...
    time.sleep(3)

    # fetch more mouse event data for processing
    data = mouse_listener.fetch_events()
    print(len(data))

    mouse_listener.stop()  # stop listening
