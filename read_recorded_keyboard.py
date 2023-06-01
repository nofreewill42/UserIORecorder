# read_recorded_keyboard.py
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd

def read_keyboard_events(data_dir='data', timestamp='latest'):
    csv_file = f'{data_dir}/{timestamp}/keyboard_events.csv' if timestamp != 'latest' else sorted(Path(data_dir).iterdir())[-1] / 'keyboard_events.csv'

    # load the data
    data = pd.read_csv(csv_file)

    event_ids = data['event'].to_numpy()
    keys = data['key'].to_numpy()
    times = data['time'].to_numpy()

    # Make the time column relative to the first timestamp
    times = times - times[0]

    # convert key names to a consistent format
    keys = np.array([key.lower() for key in keys])

    # plot the data
    fig, ax = plt.subplots()
    ax.set_xlim(0, times[-1])
    ax.set_ylim(0, len(set(keys)))

    scatter = ax.scatter(times, [list(set(keys)).index(k) for k in keys], c=event_ids, cmap='viridis', alpha=0.5)

    # add annotations
    for i, txt in enumerate(keys):
        ax.annotate(txt, (times[i], list(set(keys)).index(keys[i])))

    plt.show()

if __name__ == '__main__':
    read_keyboard_events()
