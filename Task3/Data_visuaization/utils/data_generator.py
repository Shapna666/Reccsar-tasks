import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

locations = ['A1', 'B1', 'C1', 'D1']

def generate_data(filename='data/traffic_data.csv', minutes=30):
    rows = []
    base_time = datetime.now()

    for i in range(minutes):
        timestamp = base_time + timedelta(minutes=i)
        for loc in locations:
            vehicle_count = random.randint(10, 100)
            avg_speed = round(random.uniform(20, 60), 2)
            rows.append([timestamp.strftime('%Y-%m-%d %H:%M'), loc, vehicle_count, avg_speed])
    
    df = pd.DataFrame(rows, columns=['timestamp', 'location', 'vehicle_count', 'avg_speed'])
    df.to_csv(filename, index=False)
    print(f"Generated data at {filename}")

if __name__ == "__main__":
    generate_data()
