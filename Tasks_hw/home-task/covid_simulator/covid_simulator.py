import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Load and preprocess the data
df = pd.read_csv('data.csv')
df['Date'] = pd.to_datetime(df['Date'])
region = 'RegionA'
region_data = df[df['Region'] == region].sort_values('Date')

# Normalize day numbers
region_data['Day'] = (region_data['Date'] - region_data['Date'].min()).dt.days

# Extract variables
days = region_data['Day'].values
cases = region_data['Confirmed'].values

# Exponential Growth Model
def exponential_model(x, a, b):
    return a * np.exp(b * x)

# Logistic Growth Model
def logistic_model(x, K, a, b):
    return K / (1 + a * np.exp(-b * x))

# Fit exponential model
params_exp, _ = np.polyfit(days, np.log(cases + 1), 1, cov=True)
a_exp = np.exp(params_exp[1])
b_exp = params_exp[0]
exp_pred = exponential_model(days, a_exp, b_exp)

# Fit logistic model (basic values)
K = max(cases) * 5  # Carrying capacity
a = (K - cases[0]) / cases[0]
b = 0.3  # Growth rate
log_pred = logistic_model(days, K, a, b)

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(region_data['Date'], cases, label='Actual Cases', marker='o')
plt.plot(region_data['Date'], exp_pred, label='Exponential Prediction', linestyle='--')
plt.plot(region_data['Date'], log_pred, label='Logistic Prediction', linestyle='--')
plt.title(f'COVID-19 Growth in {region}')
plt.xlabel('Date')
plt.ylabel('Confirmed Cases')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
