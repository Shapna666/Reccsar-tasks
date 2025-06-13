import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import customtkinter as ctk
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("📰 Fake News Detection Dashboard")
app.geometry("1200x700")

# Top title
title = ctk.CTkLabel(app, text="📰 Fake vs Real News Analysis Dashboard", font=ctk.CTkFont(size=22, weight="bold"))
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

def analyze_news(file_path):
    try:
        df = pd.read_csv(file_path)

        # Check required columns
        required = {'title', 'text', 'label', 'source', 'date'}
        if not required.issubset(df.columns):
            raise ValueError(f"CSV must include columns: {required}")

        df['label'] = df['label'].map({0: 'REAL', 1: 'FAKE'})  # adjust based on your dataset
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.dropna(subset=['date', 'label'])

        # Fake vs Real Count
        label_counts = df['label'].value_counts()
        fake_count = label_counts.get('FAKE', 0)
        real_count = label_counts.get('REAL', 0)

        # Source-wise distribution
        top_sources = df.groupby(['source', 'label']).size().unstack(fill_value=0).sort_values(by='FAKE', ascending=False).head(10)

        # Time-series trend
        time_series = df.set_index('date').groupby([pd.Grouper(freq='M'), 'label']).size().unstack().fillna(0)

        # Clear previous output
        output_text.configure(state="normal")
        output_text.delete("0.0", "end")
        output_text.insert("end", f"📰 Total Articles: {len(df)}\n")
        output_text.insert("end", f"✅ Real News: {real_count}\n")
        output_text.insert("end", f"❌ Fake News: {fake_count}\n\n")

        output_text.insert("end", "Top Sources Publishing Fake News:\n")
        for source, row in top_sources.iterrows():
            output_text.insert("end", f"• {source}: {row.get('FAKE', 0)} FAKE, {row.get('REAL', 0)} REAL\n")

        output_text.configure(state="disabled")

        # Clear previous charts
        for widget in chart_frame.winfo_children():
            widget.destroy()

        # Create plot
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))

        # Time-series trend
        time_series.plot(ax=axes[0], title="Fake vs Real News Over Time", color=["#EF5350", "#66BB6A"])
        axes[0].set_ylabel("Article Count")

        # Source bar chart
        top_sources.plot(kind='bar', stacked=True, ax=axes[1], color=["#EF5350", "#66BB6A"])
        axes[1].set_title("Top Sources by Fake/Real News")
        axes[1].set_ylabel("Count")

        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    except Exception as e:
        messagebox.showerror("Error", str(e))

def upload_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        analyze_news(file_path)

upload_btn = ctk.CTkButton(app, text="📂 Upload News Dataset CSV", font=("Arial", 14), command=upload_csv)
upload_btn.pack(pady=5)

app.mainloop()
