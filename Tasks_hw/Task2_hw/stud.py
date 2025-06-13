import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv("student_progress.csv")

# Step 1: Compute GPA (average score per student)
gpa_df = df.groupby("Student")["Score"].mean().reset_index()
gpa_df.columns = ["Student", "GPA"]

# Step 2: Compute Z-score and Percentile
gpa_df["Z_Score"] = (gpa_df["GPA"] - np.mean(gpa_df["GPA"])) / np.std(gpa_df["GPA"])
gpa_df["Percentile"] = gpa_df["GPA"].rank(pct=True) * 100

# Step 3: Merge GPA back to original dataframe
df = df.merge(gpa_df, on="Student")

# Step 4: Radar chart for a sample student
sample_student = df[df["Student"] == "Student_1"]
subjects = sample_student["Subject"]
scores = sample_student["Score"]

angles = np.linspace(0, 2 * np.pi, len(subjects), endpoint=False).tolist()
scores = scores.tolist()
scores += scores[:1]
angles += angles[:1]

fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111, polar=True)
ax.plot(angles, scores, 'o-', linewidth=2, label="Student_1")
ax.fill(angles, scores, alpha=0.25)
ax.set_thetagrids(np.degrees(angles[:-1]), subjects)
ax.set_title("🎯 Student_1 Subject-wise Performance (Radar Chart)")
ax.grid(True)
plt.legend(loc='upper right')
plt.tight_layout()
plt.show()

# Step 5: Heatmap of average scores per subject per class
heatmap_data = df.pivot_table(index="Class", columns="Subject", values="Score", aggfunc="mean")

plt.figure(figsize=(8, 5))
sns.heatmap(heatmap_data, annot=True, cmap="YlGnBu", linewidths=0.5)
plt.title("🔥 Average Subject Scores per Class (Heatmap)")
plt.xlabel("Subject")
plt.ylabel("Class")
plt.tight_layout()
plt.show()

# Step 6: Print GPA Summary
print("\n📊 GPA Summary (Top 5 Students):")
print(gpa_df.sort_values(by="GPA", ascending=False).head())
