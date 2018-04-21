from tkinter import DISABLED, NORMAL
from tkinter.ttk import Frame, Button


class ProcessControlFrame(Frame):
    def __init__(self, parent, start_experiment, stop_experiment):
        Frame.__init__(self, parent)

        # experiment controls
        self.start_experiment_button = None
        self.stop_experiment_button = None
        self.experiment_running = False

        # actions
        self.start_experiment = start_experiment
        self.stop_experiment = stop_experiment

        self.init_view()

    def init_view(self):
        self.start_experiment_button = Button(self, text="Start experiment", command=self.start_experiment)
        self.start_experiment_button.grid(row=0, column=3, rowspan=1)

        self.stop_experiment_button = Button(self, text="Stop experiment", command=self.stop_experiment, state=DISABLED)
        self.stop_experiment_button.grid(row=1, column=3, rowspan=1)

    def set_experiment_running(self, value):
        self.experiment_running = value
        if value is True:
            self.start_experiment_button.config(state=DISABLED)
            self.stop_experiment_button.config(state=NORMAL)
        else:
            self.start_experiment_button.config(state=NORMAL)
            self.stop_experiment_button.config(state=DISABLED)