import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
import seaborn as sns

# Simulate Crypto Transactions
np.random.seed(42)
n_normal = 1000
n_frauds = 50

# Normal transactions
normal_data = {
    'amount': np.random.normal(1000, 300, n_normal),
    'time_delta': np.random.exponential(1, n_normal),
    'transactions_last_hour': np.random.poisson(2, n_normal)
}

# Fraudulent transactions
fraud_data = {
    'amount': np.random.normal(5000, 1000, n_frauds),
    'time_delta': np.random.exponential(0.1, n_frauds),
    'transactions_last_hour': np.random.poisson(10, n_frauds)
}

# Combine data
df = pd.DataFrame(normal_data)
df['label'] = 0  # normal

df_fraud = pd.DataFrame(fraud_data)
df_fraud['label'] = 1  # fraud

df_full = pd.concat([df, df_fraud], ignore_index=True)

# Shuffle rows
df_full = df_full.sample(frac=1).reset_index(drop=True)

# Train Isolation Forest
features = ['amount', 'time_delta', 'transactions_last_hour']
X = df_full[features]

iso_forest = IsolationForest(contamination=0.05, random_state=42)
df_full['anomaly_score'] = iso_forest.fit_predict(X)
df_full['predicted'] = df_full['anomaly_score'].apply(lambda x: 1 if x == -1 else 0)

# Evaluation
conf_matrix = pd.crosstab(df_full['label'], df_full['predicted'],
                          rownames=['Actual'], colnames=['Predicted'])
print("\nConfusion Matrix:")
print(conf_matrix)

# Visualization
sns.scatterplot(data=df_full, x="amount", y="transactions_last_hour", hue="predicted", palette="coolwarm")
plt.title("Detected Anomalies in Crypto Transactions")
plt.show()
