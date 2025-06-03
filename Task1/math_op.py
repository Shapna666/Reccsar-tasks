import tkinter as tk
from math import *
import math

# Safe evaluation context
safe_dict = {k: getattr(math, k) for k in dir(math) if not k.startswith("__")}
safe_dict.update({'abs': abs, 'round': round, 'pow': pow})

def calculate_all():
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())

        # Basic operations
        add = a + b
        sub = a - b
        mul = a * b
        div = "Undefined (div by 0)" if b == 0 else round(a / b, 2)

        # Show basic operations
        operations_result = (
            f"Addition:       {a} + {b} = {add}\n"
            f"Subtraction:    {a} - {b} = {sub}\n"
            f"Multiplication: {a} * {b} = {mul}\n"
            f"Division:       {a} / {b} = {div}"
        )

        # Evaluate expression
        expr = entry_expr.get()
        if '=' in expr:
            expr = expr.split('=')[0]

        expr_result = ""
        if expr.strip():
            try:
                result = eval(expr, {"__builtins__": {}}, safe_dict)
                expr_result = f"\n\nExpression:     {expr} = {result}"
            except Exception as e:
                expr_result = f"\n\nExpression Error: {e}"

        result_label.config(text=operations_result + expr_result)

    except ValueError:
        result_label.config(text="Please enter valid numbers.")

# Setup window
root = tk.Tk()
root.title("Maths Calculator")
root.geometry("400x400")
root.resizable(False, False)

# Title
title_label = tk.Label(root, text="Maths Calculator", font=("Helvetica", 16, "bold"))
title_label.grid(row=0, column=0, columnspan=2, pady=10)

# Number A
tk.Label(root, text="Enter number A:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_a = tk.Entry(root, width=20)
entry_a.grid(row=1, column=1, padx=10, pady=5)

# Number B
tk.Label(root, text="Enter number B:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_b = tk.Entry(root, width=20)
entry_b.grid(row=2, column=1, padx=10, pady=5)

# Equation
tk.Label(root, text="Enter equation (e.g. 5+3*2=):").grid(row=3, column=0, padx=10, pady=5, sticky="e")
entry_expr = tk.Entry(root, width=20)
entry_expr.grid(row=3, column=1, padx=10, pady=5)

# Calculate button
tk.Button(root, text="Calculate", command=calculate_all, width=20).grid(row=4, column=0, columnspan=2, pady=15)

# Result output
result_label = tk.Label(root, text="", justify="left", anchor="w")
result_label.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="w")

root.mainloop()
