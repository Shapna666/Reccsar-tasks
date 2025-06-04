import tkinter as tk
from tkinter import messagebox, scrolledtext
import pandas as pd
import numpy as np

def euclidean_distance(a, b):
    return np.sqrt(np.sum((a - b) ** 2))

def run_manual_model():
    try:
        df = pd.read_csv("Iris.csv")
    except FileNotFoundError:
        messagebox.showerror("Error", "Iris.csv not found in the folder.")
        return

    output_text.delete("1.0", tk.END)

    output_text.insert(tk.END, "🌸 First 5 Rows of Dataset:\n")
    output_text.insert(tk.END, str(df.head()) + "\n\n")

    output_text.insert(tk.END, "📋 Dataset Info:\n")
    buf = []
    df.info(buf.append)
    output_text.insert(tk.END, "\n".join(buf) + "\n\n")

    output_text.insert(tk.END, "🔢 Species Count:\n")
    output_text.insert(tk.END, str(df['species'].value_counts()) + "\n\n")

    # Prepare data
    X = df.drop(columns=['species']).values
    y = df['species'].values
    unique_classes = np.unique(y)

    # Split data (manually)
    np.random.seed(42)
    indices = np.arange(len(X))
    np.random.shuffle(indices)

    train_size = int(0.8 * len(X))
    train_idx, test_idx = indices[:train_size], indices[train_size:]

    X_train, y_train = X[train_idx], y[train_idx]
    X_test, y_test = X[test_idx], y[test_idx]

    # Calculate class means
    class_means = {}
    for cls in unique_classes:
        class_means[cls] = X_train[y_train == cls].mean(axis=0)

    # Predict
    y_pred = []
    for sample in X_test:
        distances = {cls: euclidean_distance(sample, mean) for cls, mean in class_means.items()}
        predicted_class = min(distances, key=distances.get)
        y_pred.append(predicted_class)

    y_pred = np.array(y_pred)

    # Accuracy
    accuracy = np.mean(y_pred == y_test)
    output_text.insert(tk.END, f"✅ Accuracy: {accuracy * 100:.2f}%\n\n")

    # Manual classification report
    output_text.insert(tk.END, f"📊 Classification Report:\n")
    for cls in unique_classes:
        tp = np.sum((y_pred == cls) & (y_test == cls))
        fn = np.sum((y_pred != cls) & (y_test == cls))
        fp = np.sum((y_pred == cls) & (y_test != cls))
        precision = tp / (tp + fp) if (tp + fp) != 0 else 0
        recall = tp / (tp + fn) if (tp + fn) != 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) != 0 else 0

        output_text.insert(tk.END,
            f"{cls}:\n"
            f"  Precision: {precision:.2f}\n"
            f"  Recall:    {recall:.2f}\n"
            f"  F1-Score:  {f1:.2f}\n\n"
        )

# ---------------------- UI ----------------------
root = tk.Tk()
root.title("🌸 Iris Classifier (Only Numpy + Pandas)")
root.geometry("750x650")
root.configure(bg="#edf6f9")

tk.Label(root, text="🌼 Iris Classifier Using Only NumPy & Pandas 🌼", font=("Helvetica", 18, "bold"),
         fg="#006d77", bg="#edf6f9").pack(pady=20)

tk.Button(root, text="Run Classifier", command=run_manual_model, font=("Arial", 14),
          bg="#83c5be", fg="black", width=20).pack(pady=10)

output_text = scrolledtext.ScrolledText(root, width=90, height=28, font=("Courier", 10), bg="white")
output_text.pack(padx=10, pady=10)

root.mainloop()
