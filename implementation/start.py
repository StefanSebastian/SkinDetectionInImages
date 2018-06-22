import tkinter as tk
from application_gui.main_view import EvaluatorApplication
import multiprocessing

multiprocessing.freeze_support()
if __name__ == "__main__":
    win = tk.Tk()
    EvaluatorApplication(win)
    win.mainloop()
