import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load CSV file
df = pd.read_csv("expenses.csv", parse_dates=["Date"])

# Add Month column for time-based grouping
df["Month"] = df["Date"].dt.to_period("M")

# ---------------------------
# NUMPY Analysis
# ---------------------------
total_spent = np.sum(df["Amount"])
avg_spent = np.mean(df["Amount"])
std_dev = np.std(df["Amount"])

# Detect anomalies (expenses much higher than average)
threshold = avg_spent + 1.5 * std_dev
anomalies = df[df["Amount"] > threshold]

print("📊 Total Spent:", round(total_spent, 2))
print("📈 Average Transaction:", round(avg_spent, 2))
print("⚠️ Anomaly Threshold:", round(threshold, 2))
print("\n🚨 High Spending Anomalies:")
print(anomalies[["Date", "Description", "Amount", "Category"]])

# ---------------------------
# PANDAS Grouping
# ---------------------------

# Group by category
category_summary = df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
category_percent = (category_summary / total_spent) * 100

# Group by month
monthly_summary = df.groupby("Month")["Amount"].sum()

# ---------------------------
# MATPLOTLIB Visualizations
# ---------------------------

# Pie Chart - Category percentage
plt.figure(figsize=(6, 6))
category_summary.plot.pie(autopct='%1.1f%%', title="Expenses by Category")
plt.ylabel("")
plt.tight_layout()
plt.show()

# Bar Chart - Total spent per category
plt.figure(figsize=(8, 5))
category_summary.plot(kind="bar", color="skyblue")
plt.title("Total Spending by Category")
plt.xlabel("Category")
plt.ylabel("Amount Spent")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Line Chart - Monthly spending trend
plt.figure(figsize=(8, 5))
monthly_summary.plot(marker='o', linestyle='-', color='green')
plt.title("Month-on-Month Spending Trend")
plt.xlabel("Month")
plt.ylabel("Total Spent")
plt.grid(True)
plt.tight_layout()
plt.show()

# ---------------------------
# Optional: Save Reports
# ---------------------------

# Save anomaly data to CSV
anomalies.to_csv("anomaly_report.csv", index=False)

# Save summary stats
with open("summary_report.txt", "w") as f:
    f.write(f"Total Spent: {total_spent:.2f}\n")
    f.write(f"Average Transaction: {avg_spent:.2f}\n")
    f.write(f"Anomaly Threshold: {threshold:.2f}\n")
    f.write("\nTop Categories:\n")
    f.write(category_summary.to_string())
    f.write("\n\nMonthly Summary:\n")
    f.write(monthly_summary.to_string())

print("\n✅ Reports saved to 'anomaly_report.csv' and 'summary_report.txt'")
