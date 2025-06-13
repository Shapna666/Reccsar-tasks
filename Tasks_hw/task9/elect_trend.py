import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load your dataset CSV - update the filename/path if needed
df = pd.read_csv('1976-2020-president.csv')

# Keep relevant columns
df = df[['year', 'state', 'party_simplified', 'candidatevotes', 'totalvotes']]
df = df.dropna()
df = df[df['totalvotes'] > 0]

# Calculate vote share
df['vote_share'] = df['candidatevotes'] / df['totalvotes']

# Group and pivot
grouped = df.groupby(['year', 'party_simplified'])['vote_share'].mean().reset_index()
pivot_df = grouped.pivot(index='year', columns='party_simplified', values='vote_share').fillna(0)

# Total votes per year
total_votes_yearly = df.groupby('year')['totalvotes'].sum()

# Create subplots (3 rows, 1 column)
fig, axs = plt.subplots(3, 1, figsize=(14, 16))

# 1. Line plot: vote share trends
for party in pivot_df.columns:
    axs[0].plot(pivot_df.index, pivot_df[party], label=party)
axs[0].set_title("Average Vote Share by Party Over Time")
axs[0].set_xlabel("Year")
axs[0].set_ylabel("Average Vote Share")
axs[0].legend()
axs[0].grid(True)

# 2. Stacked area chart
axs[1].stackplot(pivot_df.index, pivot_df.T, labels=pivot_df.columns)
axs[1].set_title("Stacked Vote Share Area Chart by Party")
axs[1].set_xlabel("Year")
axs[1].set_ylabel("Vote Share")
axs[1].legend(loc='upper left')
axs[1].grid(True)

# 3. Total votes line plot
axs[2].plot(total_votes_yearly.index, total_votes_yearly.values, marker='o', color='purple')
axs[2].set_title("Total Votes Cast Over Time")
axs[2].set_xlabel("Year")
axs[2].set_ylabel("Total Votes")
axs[2].grid(True)

# Adjust spacing
plt.tight_layout()
plt.show()
