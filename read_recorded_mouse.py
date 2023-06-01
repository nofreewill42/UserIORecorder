import struct
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from pathlib import Path

format = 'bhhd'

# load the data
record_size = struct.calcsize(format)
binary_data = Path('data/mouse_events.bin').read_bytes()
num_records = len(binary_data)//record_size
num_bytes = num_records*record_size
binary_data = binary_data[:num_bytes]  # remove last incomplete record if there is one, for example when the program was terminated while recording

# convert the data to a numpy array
event_ids = []
xs, ys = [], []
times = []
for i in range(num_records):
    record = binary_data[i*record_size:(i+1)*record_size]
    event_id, x, y, time = struct.unpack(format, record)
    event_ids.append(event_id)
    xs.append(x)
    ys.append(y)
    times.append(time)
event_ids_np = np.array(event_ids)
xs_np = np.array(xs)
ys_np = np.array(ys)
times_np = np.array(times)

# plot the data
fig, ax = plt.subplots()
ax.set_xlim(0, 1920*2)
ax.set_ylim(0, 1080)

plt.scatter(xs_np, ys_np, c=times_np, cmap='viridis', alpha=0.5)
plt.show()