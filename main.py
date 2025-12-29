import tkinter as tk
from gui import TaskTrackerApp

def main():
    root = tk.Tk()
    app = TaskTrackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()