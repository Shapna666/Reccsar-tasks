import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import customtkinter as ctk
from tkinter import filedialog, messagebox, Toplevel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tabulate import tabulate

# Setup UI
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("🏃 Fitness Tracker Analyzer")
app.geometry("1200x700")

title = ctk.CTkLabel(app, text="🏃‍♂️ Fitness Performance Dashboard", font=ctk.CTkFont(size=22, weight="bold"))
title.pack(pady=15)

main_frame = ctk.CTkFrame(app)
main_frame.pack(fill="both", expand=True, padx=20, pady=10)

output_frame = ctk.CTkFrame(main_frame)
output_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

chart_frame = ctk.CTkFrame(main_frame)
chart_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

output_text = ctk.CTkTextbox(output_frame, font=("Consolas", 12), wrap="word")
output_text.pack(fill="both", expand=True)
output_text.configure(state="disabled")

global_df = None  # Store full DataFrame for "Show Raw Data"


def analyze_fitness(file_path):
    global global_df
    try:
        df = pd.read_csv(file_path)
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.sort_values("Date")
        global_df = df  # Save globally for later viewing

        # Weekly grouping
        df["Week"] = df["Date"].dt.isocalendar().week
        weekly = df.groupby("Week").agg({
            "Steps": ["mean", "sum", "max"],
            "Calories Burned": ["mean", "sum"],
            "Average Heart Rate": ["mean", "max"]
        }).round(2)

        avg_steps = np.mean(df["Steps"])
        peak_day = df.loc[df["Steps"].idxmax(), "Date"].strftime('%Y-%m-%d')
        high_hr_day = df.loc[df["Average Heart Rate"].idxmax(), "Date"].strftime('%Y-%m-%d')

        # Display textual summary
        output_text.configure(state="normal")
        output_text.delete("0.0", "end")
        output_text.insert("end", f"📅 Total Days Tracked: {len(df)}\n")
        output_text.insert("end", f"👣 Average Daily Steps: {avg_steps:.2f}\n")
        output_text.insert("end", f"🏆 Peak Activity Day: {peak_day}\n")
        output_text.insert("end", f"❤️ Highest Heart Rate Day: {high_hr_day}\n\n")
        output_text.insert("end", f"📊 Weekly Summary:\n")

        summary_table = tabulate(weekly, headers="keys", tablefmt="fancy_grid", showindex=True)
        output_text.insert("end", summary_table)
        output_text.configure(state="disabled")

        # Clear old plots
        for widget in chart_frame.winfo_children():
            widget.destroy()

        # Create plots
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        df.plot(x="Date", y="Steps", ax=axes[0], title="Daily Steps", color="#4CAF50", marker='o')
        axes[0].set_ylabel("Steps")

        df.plot(x="Date", y="Calories Burned", ax=axes[1], title="Daily Calories Burned", color="#FF9800", marker='o')
        axes[1].set_ylabel("Calories")

        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    except Exception as e:
        messagebox.showerror("Error", str(e))


def upload_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        analyze_fitness(file_path)


def show_raw_data():
    if global_df is None:
        messagebox.showwarning("Warning", "Upload a CSV file first!")
        return

    raw_window = Toplevel(app)
    raw_window.title("📈 Raw Time-Series Data")
    raw_window.geometry("600x400")

    raw_box = ctk.CTkTextbox(raw_window, font=("Consolas", 12), wrap="none")
    raw_box.pack(fill="both", expand=True, padx=10, pady=10)

    raw_box.insert("end", global_df.to_string(index=False))
    raw_box.configure(state="disabled")


# Buttons
btn_frame = ctk.CTkFrame(app)
btn_frame.pack(pady=10)

upload_btn = ctk.CTkButton(btn_frame, text="📂 Upload Fitness CSV", font=("Arial", 14), command=upload_csv)
upload_btn.pack(side="left", padx=10)

view_raw_btn = ctk.CTkButton(btn_frame, text="🔍 Show Raw Time-Series Data", font=("Arial", 14), command=show_raw_data)
view_raw_btn.pack(side="left", padx=10)

app.mainloop()
