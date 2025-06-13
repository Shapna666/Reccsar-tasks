import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# RDI (Recommended Daily Intake)
nutrient_labels = [
    "Calories", "Protein(g)", "Fat(g)", "Carbs(g)",
    "Vitamin A(mcg)", "Vitamin C(mg)", "Calcium(mg)", "Iron(mg)"
]
rdi = np.array([2000, 50, 70, 310, 900, 90, 1000, 18])

# Main app window
root = tk.Tk()
root.title("Daily Food Nutrient Analyzer")
root.geometry("1200x650")
root.configure(bg="#f0fff0")

# Top title
title = tk.Label(root, text="🍽️ Daily Nutrient Analysis Tool", font=("Helvetica", 22, "bold"), bg="#f0fff0", fg="#1b5e20")
title.pack(pady=10)

# Frame layout
main_frame = tk.Frame(root, bg="#f0fff0")
main_frame.pack(fill="both", expand=True, padx=20, pady=10)

# Output Text Area
output_frame = tk.LabelFrame(main_frame, text="📝 Nutrient Report", bg="white", fg="green", font=("Arial", 12, "bold"))
output_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

scrollbar = tk.Scrollbar(output_frame)
scrollbar.pack(side="right", fill="y")

output_text = tk.Text(output_frame, wrap="word", yscrollcommand=scrollbar.set, font=("Courier", 11), bg="white", fg="black")
output_text.pack(fill="both", expand=True)
scrollbar.config(command=output_text.yview)

# Chart Frame
chart_frame = tk.LabelFrame(main_frame, text="📊 Visual Summary", font=("Arial", 12, "bold"), bg="white", fg="green")
chart_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

def analyze_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.strip()

        # Ensure all nutrient columns are numeric
        for col in nutrient_labels:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        df = df.dropna(subset=nutrient_labels)
        grouped = df.groupby("Category").sum(numeric_only=True)

        # Calculations
        totals = df[nutrient_labels].sum().values
        percent = (totals / rdi) * 100
        deficiency = rdi - totals
        deficient_nutrients = [nutrient_labels[i] for i, d in enumerate(deficiency) if d > 0]

        # Output Report
        output_text.config(state="normal")
        output_text.delete("1.0", "end")

        output_text.insert("end", "🧾 Total Nutrients Consumed:\n\n")
        for i in range(len(nutrient_labels)):
            output_text.insert("end", f"• {nutrient_labels[i]}: {totals[i]:.2f}\n")

        output_text.insert("end", "\n✅ % of Daily Requirement Met:\n\n")
        for i in range(len(nutrient_labels)):
            output_text.insert("end", f"• {nutrient_labels[i]}: {percent[i]:.1f}%\n")

        output_text.insert("end", "\n🚨 Deficient Nutrients:\n\n")
        if deficient_nutrients:
            for item in deficient_nutrients:
                output_text.insert("end", f"• {item}\n")
        else:
            output_text.insert("end", "🎉 No deficiencies found!")

        output_text.config(state="disabled")

        # Draw chart
        for widget in chart_frame.winfo_children():
            widget.destroy()

        fig, axes = plt.subplots(1, 2, figsize=(10, 4))

        axes[0].bar(nutrient_labels, percent, color="#66BB6A")
        axes[0].axhline(100, color="red", linestyle="--")
        axes[0].set_title("Nutrient Intake (%)")
        axes[0].tick_params(axis='x', rotation=45)

        grouped["Calories"].plot.pie(autopct='%1.1f%%', startangle=90, ax=axes[1])
        axes[1].set_title("Calories by Food Group")
        axes[1].set_ylabel("")

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{str(e)}")

def upload_csv():
    path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if path:
        analyze_csv(path)

upload_btn = ttk.Button(root, text="📂 Upload Food CSV", command=upload_csv)
upload_btn.pack(pady=5)

root.mainloop()
 