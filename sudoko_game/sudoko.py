import tkinter as tk
from tkinter import messagebox

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver with AI Logic")
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.build_ui()

    def build_ui(self):
        frame = tk.Frame(self.root)
        frame.pack()

        for i in range(9):
            for j in range(9):
                e = tk.Entry(frame, width=3, font=("Arial", 18), justify='center')
                e.grid(row=i, column=j, padx=1, pady=1)
                self.entries[i][j] = e

        solve_button = tk.Button(self.root, text="Solve", command=self.solve)
        solve_button.pack(pady=10)

    def get_board(self):
        board = []
        for i in range(9):
            row = []
            for j in range(9):
                val = self.entries[i][j].get()
                row.append(int(val) if val.isdigit() else 0)
            board.append(row)
        return board

    def set_board(self, board):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                if board[i][j] != 0:
                    self.entries[i][j].insert(0, str(board[i][j]))

    def solve(self):
        board = self.get_board()
        if solve_sudoku(board):
            self.set_board(board)
        else:
            messagebox.showerror("Error", "No solution exists!")

# Sudoku logic functions (same as before)

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def is_valid(board, num, pos):
    row, col = pos

    for i in range(9):
        if board[row][i] == num and i != col:
            return False
        if board[i][col] == num and i != row:
            return False

    box_x = col // 3 * 3
    box_y = row // 3 * 3

    for i in range(box_y, box_y + 3):
        for j in range(box_x, box_x + 3):
            if board[i][j] == num and (i, j) != pos:
                return False

    return True

def solve_sudoku(board):
    empty = find_empty(board)
    if not empty:
        return True
    row, col = empty

    for num in range(1, 10):
        if is_valid(board, num, (row, col)):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0

    return False

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()
