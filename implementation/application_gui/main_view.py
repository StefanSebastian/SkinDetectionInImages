import tkinter as tk
from tkinter.ttk import Notebook, Frame

from application_gui.detection_view import DetectionFrame
from application_gui.evaluation_view import EvaluationFrame
from application_gui.train_spm_view import TrainSpmFrame
from application_gui.train_texture_view import TrainTextureFrame


class EvaluatorApplication(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.create_windows()

    def create_windows(self):
        notebook = Notebook(self.master)

        tab_evaluation = Frame(notebook)
        notebook.add(tab_evaluation, text="Evaluator")
        EvaluationFrame(tab_evaluation)

        tab_train_spm = Frame(notebook)
        notebook.add(tab_train_spm, text="Train SPM")
        TrainSpmFrame(tab_train_spm)

        tab_train_texture = Frame(notebook)
        notebook.add(tab_train_texture, text="Train texture")
        TrainTextureFrame(tab_train_texture)

        tab_detection = Frame(notebook)
        notebook.add(tab_detection, text="Detection")
        DetectionFrame(tab_detection)

        notebook.pack(expand=1, fill="both")

if __name__ == '__main__':
    win = tk.Tk()
    EvaluatorApplication(win)
    win.mainloop()
