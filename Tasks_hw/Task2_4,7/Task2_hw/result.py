import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load temperature data
temp_df = pd.read_csv("temperature.csv", parse_dates=["dt"])
temp_df.rename(columns={"dt": "Date"}, inplace=True)

# Load pollution data
poll_df = pd.read_csv("pollution.csv")

# Clean column names
poll_df.columns = poll_df.columns.str.strip().str.replace('"', '')

# Convert date in temperature to only date part
temp_df["Date"] = temp_df["Date"].dt.date

# Select necessary columns and clean
temp_df = temp_df[["City", "Country", "Date", "AverageTemperature"]]
poll_df = poll_df.rename(columns={
    "city_name": "City",
    "country_name": "Country",
    "pm2.5_aqi_value": "PM2.5",
    "no2_aqi_value": "NO2",
    "co_aqi_value": "CO",
})

# Drop NA values
temp_df.dropna(subset=["AverageTemperature"], inplace=True)
poll_df.dropna(subset=["PM2.5", "NO2", "CO"], inplace=True)

# Optional: Round or parse to match city names if needed

# Merge the data on City and Country (date might not match if pollution data has no date)
df = pd.merge(temp_df, poll_df, on=["City", "Country"])

# Calculate AQI index manually using dummy weights
df["AQI"] = 0.5 * df["PM2.5"] + 0.3 * df["NO2"] + 0.2 * df["CO"]

# Calculate deviation from mean AQI using NumPy
df["AQI_Deviation"] = df.groupby("City")["AQI"].transform(lambda x: np.abs(x - np.mean(x)))

# Create pivot tables for heatmaps
aqi_pivot = df.pivot_table(index="Date", columns="City", values="AQI")
temp_pivot = df.pivot_table(index="Date", columns="City", values="AverageTemperature")

# Plotting the heatmaps
plt.figure(figsize=(14, 6))

# AQI Heatmap
plt.subplot(1, 2, 1)
sns.heatmap(aqi_pivot, cmap="Reds", linewidths=0.5)
plt.title("🔴 AQI Heatmap by City and Date")
plt.xlabel("City")
plt.ylabel("Date")

# Temperature Heatmap
plt.subplot(1, 2, 2)
sns.heatmap(temp_pivot, cmap="YlGnBu", linewidths=0.5)
plt.title("🔵 Temperature Heatmap by City and Date")
plt.xlabel("City")
plt.ylabel("Date")

plt.tight_layout()
plt.show()

# Print summary stats
print("\n🌆 Summary Statistics by City:")
summary = df.groupby("City")[["AverageTemperature", "AQI", "AQI_Deviation"]].mean().round(2)
print(summary)
