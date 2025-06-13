# teacher.py
import tkinter as tk
from chatbot import open_chatbot
from student import enrolled_courses
from assets.style_utils import *
import subprocess

def open_teacher_dashboard(username):
    dashboard = tk.Tk()
    dashboard.title(f"{username}'s Teacher Dashboard")
    dashboard.geometry("600x500")
    dashboard.configure(bg=BG_LIGHT)

    tk.Label(dashboard, text=f"Welcome, {username}", font=FONT_HEADER, bg=BG_LIGHT).pack(pady=10)
    tk.Label(dashboard, text="Enrollment Overview", font=FONT_SUB, bg=BG_LIGHT).pack()

    # 🖱️ Scrollable Frame
    canvas = tk.Canvas(dashboard, bg=BG_LIGHT, borderwidth=0, highlightthickness=0, height=300)
    frame = tk.Frame(canvas, bg=BG_LIGHT)
    vsb = tk.Scrollbar(dashboard, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)

    vsb.pack(side="right", fill="y")
    canvas.pack(fill="both", expand=True)
    canvas.create_window((0, 0), window=frame, anchor="nw")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame.bind("<Configure>", on_frame_configure)

    if enrolled_courses:
        for course in enrolled_courses:
            row = tk.Frame(frame, bg=BG_LIGHT)
            row.pack(anchor="w", padx=20, pady=3)
            tk.Label(row, text=f"📘 {course}", font=FONT_NORMAL, bg=BG_LIGHT).pack(side="left")
    else:
        tk.Label(frame, text="No students enrolled yet.", font=FONT_NORMAL, bg=BG_LIGHT).pack()

    tk.Button(dashboard, text="Ask Chatbot 🤖", font=FONT_NORMAL, bg=BUTTON_BLUE, fg=BUTTON_WHITE,
              command=lambda: open_chatbot("Teacher")).pack(pady=5)

    tk.Button(dashboard, text="Back to Login", font=FONT_SMALL, bg=BUTTON_WHITE,
              command=lambda: [dashboard.destroy(), subprocess.Popen(["python", "main.py"])]).pack(pady=5)

    dashboard.mainloop()
