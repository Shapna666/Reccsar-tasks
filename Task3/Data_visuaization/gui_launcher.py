import tkinter as tk
from tkinter import messagebox
from plots.seaborn_plot import seaborn_heatmap
from plots.matplotlib_plot import live_matplotlib_plot
from plots.plotly_live import plotly_animated_plot
from utils.data_generator import generate_data

# ------------------------
# GUI Setup
# ------------------------
def launch_seaborn():
    try:
        seaborn_heatmap()
    except Exception as e:
        messagebox.showerror("Error", f"Seaborn Plot Failed:\n{e}")

def launch_matplotlib():
    try:
        live_matplotlib_plot()
    except Exception as e:
        messagebox.showerror("Error", f"Matplotlib Plot Failed:\n{e}")

def launch_plotly():
    try:
        plotly_animated_plot()
    except Exception as e:
        messagebox.showerror("Error", f"Plotly Plot Failed:\n{e}")

def generate_traffic_data():
    try:
        generate_data()
        messagebox.showinfo("Success", "Sample traffic data generated!")
    except Exception as e:
        messagebox.showerror("Error", f"Data Generation Failed:\n{e}")

# Create main window
app = tk.Tk()
app.title("🚦 Real-Time Traffic Visualizer")
app.geometry("420x400")
app.configure(bg="#d8f3dc")  # Light pastel green

# Heading
header = tk.Label(app, text="🛣️  Traffic Data Visualizer", font=("Helvetica", 18, "bold"), bg="#d8f3dc", fg="#1b4332")
header.pack(pady=20)

# Buttons
btn_generate = tk.Button(app, text="📊 Generate Traffic Data", command=generate_traffic_data, bg="#52b788", fg="white", font=("Arial", 12), width=30, pady=5)
btn_generate.pack(pady=10)

btn1 = tk.Button(app, text="🔥 View Seaborn Heatmap", command=launch_seaborn, bg="#40916c", fg="white", font=("Arial", 12), width=30, pady=5)
btn1.pack(pady=10)

btn2 = tk.Button(app, text="📈 View Matplotlib Live Graph", command=launch_matplotlib, bg="#2d6a4f", fg="white", font=("Arial", 12), width=30, pady=5)
btn2.pack(pady=10)

btn3 = tk.Button(app, text="🚗 View Plotly Animation", command=launch_plotly, bg="#1b4332", fg="white", font=("Arial", 12), width=30, pady=5)
btn3.pack(pady=10)

# Run the app
app.mainloop()
