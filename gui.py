import tkinter as tk
from tkinter import ttk, messagebox

class TaskTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Задачник")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskTrackerApp(root)
    root.mainloop()