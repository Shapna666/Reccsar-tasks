import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def seaborn_heatmap(datafile='data/traffic_data.csv'):
    df = pd.read_csv(datafile)
    pivot_df = df.pivot_table(index='location', columns='timestamp', values='vehicle_count')

    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot_df, cmap='Reds', annot=True, fmt='g')
    plt.title('Traffic Congestion Heatmap')
    plt.ylabel('Location')
    plt.xlabel('Time')
    plt.tight_layout()
    plt.show()
