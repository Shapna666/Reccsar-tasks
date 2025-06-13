import pandas as pd
import matplotlib.pyplot as plt
import time

def live_matplotlib_plot(datafile='data/traffic_data.csv'):
    df = pd.read_csv(datafile)

    # Ensure timestamps are in datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Get list of unique timestamps (sorted)
    timestamps = sorted(df['timestamp'].unique())
    locations = df['location'].unique()

    # Set up plot
    plt.ion()  # Interactive mode ON
    fig, ax = plt.subplots()
    lines = {}

    for loc in locations:
        # Initialize one line per location
        lines[loc], = ax.plot([], [], label=loc)

    ax.set_xlim(0, len(timestamps))
    ax.set_ylim(0, df['vehicle_count'].max() + 10)
    ax.set_title("Live Traffic Plot")
    ax.set_xlabel("Time Step")
    ax.set_ylabel("Vehicle Count")
    ax.legend()

    x_vals = []
    y_vals = {loc: [] for loc in locations}

    for i, ts in enumerate(timestamps):
        frame = df[df['timestamp'] == ts]
        x_vals.append(i)

        for loc in locations:
            count = frame[frame['location'] == loc]['vehicle_count']
            val = int(count.values[0]) if not count.empty else 0
            y_vals[loc].append(val)
            lines[loc].set_data(x_vals, y_vals[loc])

        ax.set_xlim(0, len(x_vals))
        plt.pause(0.5)

    plt.ioff()
    plt.show()
