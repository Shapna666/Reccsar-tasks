# student.py
import tkinter as tk
from tkinter import messagebox
from chatbot import open_chatbot
from assets.style_utils import *
import subprocess

COURSES = [f"Course {i+1}: Python Basics Level {i+1}" for i in range(20)]
enrolled_courses = []

def enroll(course, username, refresh_callback):
    if course not in enrolled_courses:
        enrolled_courses.append(course)
        messagebox.showinfo("Enrolled", f"{username} enrolled in:\n{course}")
        refresh_callback()
    else:
        messagebox.showwarning("Already Enrolled", "You have already enrolled in this course.")

def open_student_dashboard(username):
    dashboard = tk.Tk()
    dashboard.title(f"{username}'s Student Dashboard")
    dashboard.geometry("600x500")
    dashboard.configure(bg=BG_SECONDARY)

    tk.Label(dashboard, text=f"Welcome, {username}", font=FONT_HEADER, bg=BG_SECONDARY).pack(pady=10)
    tk.Label(dashboard, text="Available Courses", font=FONT_SUB, bg=BG_SECONDARY).pack()

    # Canvas and scrollbar
    canvas = tk.Canvas(dashboard, bg=BG_SECONDARY, borderwidth=0, highlightthickness=0, height=300)
    frame = tk.Frame(canvas, bg=BG_SECONDARY)
    vsb = tk.Scrollbar(dashboard, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)

    vsb.pack(side="right", fill="y")
    canvas.pack(fill="both", expand=True)
    canvas.create_window((0, 0), window=frame, anchor="nw")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame.bind("<Configure>", on_frame_configure)

    # ✅ Refresh course list
    def refresh():
        for widget in frame.winfo_children():
            widget.destroy()
        for course in COURSES:
            row = tk.Frame(frame, bg=BG_SECONDARY)
            row.pack(anchor="w", padx=20, pady=3)
            tk.Label(row, text=course, font=FONT_NORMAL, bg=BG_SECONDARY).pack(side="left")
            if course in enrolled_courses:
                tk.Label(row, text="Enrolled ✅", font=FONT_SMALL, bg=BG_SECONDARY, fg="green").pack(side="right", padx=10)
            else:
                tk.Button(row, text="Enroll", font=FONT_SMALL, bg=BUTTON_GREEN, fg=BUTTON_WHITE,
                          command=lambda c=course: enroll(c, username, refresh)).pack(side="right", padx=10)

    refresh()

    # 🤖 Chatbot and 🔙 Back to Login buttons
    tk.Button(dashboard, text="Ask Chatbot 🤖", font=FONT_NORMAL, bg=BUTTON_BLUE, fg=BUTTON_WHITE,
              command=lambda: open_chatbot("Student")).pack(pady=5)

    tk.Button(dashboard, text="Back to Login", font=FONT_SMALL, bg=BUTTON_WHITE,
              command=lambda: [dashboard.destroy(), subprocess.Popen(["python", "main.py"])]).pack(pady=5)

    dashboard.mainloop()
