import tkinter as tk
from tkinter import ttk
from sympy import symbols, sympify, diff, integrate
import math

x = symbols('x')  # Symbol for calculus

def safe_eval(expr):
    try:
        expr = expr.replace("^", "**")
        expr = expr.replace("sin(", "math.sin(math.radians(")
        expr = expr.replace("cos(", "math.cos(math.radians(")
        expr = expr.replace("tan(", "math.tan(math.radians(")
        return eval(expr, {"__builtins__": None, "math": math})
    except Exception as e:
        return f"Error: {e}"

def process():
    expr = expr_entry.get()
    operation = operation_combo.get()

    try:
        if operation == "Evaluate":
            result = safe_eval(expr)
        elif operation == "Derivative":
            result = diff(sympify(expr), x)
        elif operation == "Integral":
            result = integrate(sympify(expr), x)
        elif operation == "Addition":
            a, b = map(float, expr.split(','))
            result = a + b
        elif operation == "Subtraction":
            a, b = map(float, expr.split(','))
            result = a - b
        elif operation == "Multiplication":
            a, b = map(float, expr.split(','))
            result = a * b
        elif operation == "Division":
            a, b = map(float, expr.split(','))
            result = a / b if b != 0 else "Error: Division by zero"
        else:
            result = "Unknown operation"
        result_label.config(text=f"Result: {result}", bg="#f0f0f0")
    except Exception as e:
        result_label.config(text=f"Error: {e}", bg="#f0f0f0")

# Tkinter GUI
root = tk.Tk()
root.title("Maths Calculator")
root.geometry("600x400")
root.configure(bg="#dff6ff")

tk.Label(root, text="📐 Maths Calculator 📊", font=("Helvetica", 20, "bold"), fg="#1b4965", bg="#dff6ff").pack(pady=20)

frame = tk.Frame(root, bg="#dff6ff")
frame.pack(pady=10)

tk.Label(frame, text="Expression/Input:", font=("Arial", 12), bg="#dff6ff").grid(row=0, column=0, padx=10, pady=5, sticky="e")
expr_entry = tk.Entry(frame, width=40, font=("Arial", 12))
expr_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame, text="Operation:", font=("Arial", 12), bg="#dff6ff").grid(row=1, column=0, padx=10, pady=5, sticky="e")
operation_combo = ttk.Combobox(frame, font=("Arial", 12), width=37, values=[
    "Evaluate", "Derivative", "Integral", 
    "Addition", "Subtraction", "Multiplication", "Division"
])
operation_combo.grid(row=1, column=1, padx=10, pady=5)
operation_combo.current(0)

tk.Button(root, text="Calculate", command=process, font=("Arial", 12, "bold"), bg="#1b4965", fg="white", width=20).pack(pady=15)

result_label = tk.Label(root, text="", font=("Courier", 14), bg="#f0f0f0", width=60, height=4, wraplength=500, justify="left")
result_label.pack(pady=10)

root.mainloop()