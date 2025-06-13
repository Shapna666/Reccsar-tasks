# main.py
import tkinter as tk
from tkinter import messagebox
from student import open_student_dashboard
from teacher import open_teacher_dashboard
from assets.style_utils import *

def login():
    username = entry_username.get()
    password = entry_password.get()
    role = role_var.get()

    if not username.strip() or not password.strip():
        messagebox.showerror("Error", "Please enter both username and password.")
        return

    root.destroy()
    if role == "Student":
        open_student_dashboard(username)
    else:
        open_teacher_dashboard(username)

root = tk.Tk()
root.title("LMS Login")
root.geometry("400x350")
root.configure(bg=BG_LIGHT)

tk.Label(root, text="Learning Management System", font=FONT_HEADER, bg=BG_LIGHT).pack(pady=15)

tk.Label(root, text="Username:", font=FONT_NORMAL, bg=BG_LIGHT).pack()
entry_username = tk.Entry(root, font=FONT_NORMAL)
entry_username.pack(pady=5)

tk.Label(root, text="Password:", font=FONT_NORMAL, bg=BG_LIGHT).pack()
entry_password = tk.Entry(root, show="*", font=FONT_NORMAL)
entry_password.pack(pady=5)

# Role selection
tk.Label(root, text="Login as:", font=FONT_NORMAL, bg=BG_LIGHT).pack(pady=10)
role_var = tk.StringVar(value="Student")

tk.Radiobutton(root, text="Student", variable=role_var, value="Student", font=FONT_SMALL, bg=BG_LIGHT).pack()
tk.Radiobutton(root, text="Teacher", variable=role_var, value="Teacher", font=FONT_SMALL, bg=BG_LIGHT).pack()

# Login Button
tk.Button(root, text="Login", font=FONT_NORMAL, bg=BUTTON_GREEN, fg=BUTTON_WHITE, command=login).pack(pady=15)

root.mainloop()
