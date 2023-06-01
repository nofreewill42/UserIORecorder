# read_recorded_keyboard.py
import struct
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from pathlib import Path

def read_keyboard_events(data_dir='data', timestamp='latest'):
    format = 'bid'
    bin_file = f'{data_dir}/{timestamp}/keyboard_events.bin' if timestamp != 'latest' else sorted(Path(data_dir).iterdir())[-1] / 'keyboard_events.bin'

    # load the data
    record_size = struct.calcsize(format)
    binary_data = Path(bin_file).read_bytes()
    num_records = len(binary_data)//record_size
    num_bytes = num_records*record_size
    binary_data = binary_data[:num_bytes]  # remove last incomplete record if there is one, for example when the program was terminated while recording

    # convert the data to a numpy array
    event_ids = []
    keys = []
    times = []
    for i in range(num_records):
        record = binary_data[i*record_size:(i+1)*record_size]
        event_id, key, time = struct.unpack(format, record)
        event_ids.append(event_id)
        keys.append(key)
        times.append(time)
    event_ids_np = np.array(event_ids)
    keys_np = np.array(keys)
    times_np = np.array(times)

    # plot the data
    fig, ax = plt.subplots()
    ax.set_xlabel("Time")
    ax.set_ylabel("Key Code")

    plt.scatter(times_np, keys_np, c=event_ids_np, cmap='viridis', alpha=0.5)
    plt.show()

if __name__ == '__main__':
    read_keyboard_events()
