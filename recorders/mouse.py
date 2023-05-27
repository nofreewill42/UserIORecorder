import atexit
import struct

import time
from pynput.mouse import Controller, Listener


class MouseListener:
    def __init__(self, delta_time=None):
        self.mouse = Controller()
        self.prev_position = self.mouse.position
        self.delta_time = delta_time
        self.start_time = time.time()
        self.prev_time = self.start_time  # used to check if the mouse has moved more than delta_time

        self.bin_file = open('data/mouse_events.bin', 'wb')
        atexit.register(self.bin_file.close)  # make sure the file is being closed when the program exits

        self.event2id = {'move':0,
                         'click_left_press':1,
                         'click_left_release':2,
                         'click_right_press':3,
                         'click_right_release':4,
                         'scroll':5}

    def write_row(self, event_id, x, y, time):
        binary_data = struct.pack('bhhd', event_id, x, y, time)  # b: byte, h: short, f: float; for unsigned use B, H
        self.bin_file.write(binary_data)
    
    def get_time(self):
        return time.time()# - self.start_time

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

            print(f'Event: {event_id}, Position: {current_position}, Time: {current_time}')

            self.write_row(event_id, x, y, current_time)

    
    def on_click(self, x, y, button, pressed):
        current_time = self.get_time()
        event_id = -1  # default value : unknown event
        if button == button.left:
            if pressed:
                event_id = self.event2id[f'click_left_press']
            else:
                event_id = self.event2id[f'click_left_release']
        elif button == button.right:
            if pressed:
                event_id = self.event2id[f'click_right_press']
            else:
                event_id = self.event2id[f'click_right_release']

        print(f'Event: {event_id}, Position: {(x, y)}, Time: {current_time}')

        self.write_row(event_id, x, y, current_time)

    def on_scroll(self, x, y, dx, dy):
        current_time = self.get_time()
        event_id = self.event2id['scroll']

        print(f'Event: {event_id}, difference: {(dx, dy)}, Time: {current_time}')

        self.write_row(event_id, dx, dy, current_time)
        
    
    def start(self):
        with Listener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll) as listener:
            listener.join()
    