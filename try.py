import time
import pyxhook

# This function will be called every time a key is pressed
def key_down_event(event):
    current_time = time.time()
    if event.Key in pressed_keys:
        return
    pressed_keys.add(event.Key)
    print('Event:', 0)
    print('Key:', event.Key)
    print('ASCII:', event.Ascii)
    print('Time:', current_time)

def key_up_event(event):
    current_time = time.time()
    pressed_keys.discard(event.Key)
    print('Event:', 1)
    print('Key:', event.Key)
    print('ASCII:', event.Ascii)
    print('Time:', current_time)

# Create a hook manager
hookman = pyxhook.HookManager()

# Define our callback to fire when a key is pressed down
hookman.KeyDown = key_down_event
hookman.KeyUp = key_up_event

# Hook the keyboard
hookman.HookKeyboard()

# Start our listener
hookman.start()

# Keep track of keys that are currently being pressed
pressed_keys = set()

# Create a loop to keep the application running
while True:
    pass  # time.sleep(0.1)
