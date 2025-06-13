import pandas as pd
import plotly.express as px
import plotly.io as pio

def plotly_animated_plot(datafile='data/traffic_data.csv'):
    # Set renderer for non-notebook environments
    pio.renderers.default = 'browser'

    df = pd.read_csv(datafile)
    df.dropna(inplace=True)
    df['timestamp'] = df['timestamp'].astype(str)
    df.sort_values(by=['timestamp', 'location'], inplace=True)

    fig = px.line(
        df,
        x="timestamp",
        y="vehicle_count",
        color="location",
        animation_frame="timestamp",
        title="Real-Time Traffic Animation (Plotly)",
        markers=True
    )

    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Vehicle Count",
        transition_duration=300
    )

    fig.show()
