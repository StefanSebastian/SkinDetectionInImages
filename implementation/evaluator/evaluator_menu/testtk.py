import tkinter
from tkinter import Tk, Text, TOP, BOTH, X, N, LEFT, IntVar
from tkinter.ttk import Frame, Label, Entry, Checkbutton, Button, Separator
from tkinter import filedialog


from evaluator.run_configuration import RunConfiguration
from evaluator.simulation import Evaluator

import threading

from utils.log import CompositeLogger, ConsoleLogger, FileLogger


class EvaluatorMenu(Frame):
    def __init__(self):
        super().__init__()

        self.configuration = RunConfiguration()
        self.sigma_in = None
        self.tau_in = None
        self.position_in = None

        self.spm_model_path_in = None

        self.init_ui()

    def init_ui(self):
        self.master.title("Review")
        self.pack(fill=BOTH, expand=True)

        self.build_segmentation_frame()
        self.build_spm_frame()

        start_experiment_button = Button(text="Start experiment", command=self.start_experiment)
        start_experiment_button.pack()

    def build_segmentation_frame(self):
        segmentation_frame = Frame(self, borderwidth=1, relief=tkinter.GROOVE)
        segmentation_frame.pack(fill=X)

        segmentation_label = Label(segmentation_frame, text="Segmentation")
        segmentation_label.pack(side=LEFT, padx=5, pady=5)

        sigma_frame = Frame(segmentation_frame)
        sigma_frame.pack(fill=X)
        sigma_label = Label(sigma_frame, text="Sigma")
        sigma_label.pack(side=LEFT, padx=5, pady=5)
        self.sigma_in = Entry(sigma_frame)
        self.sigma_in.pack(fill=X, padx=5, expand=True)

        tau_frame = Frame(segmentation_frame)
        tau_frame.pack(fill=X)
        tau_label = Label(tau_frame, text="Tau")
        tau_label.pack(side=LEFT, padx=5, pady=5)
        self.tau_in = Entry(tau_frame)
        self.tau_in.pack(fill=X, padx=5, expand=True)

        position_frame = Frame(segmentation_frame)
        position_frame.pack(fill=X)
        v = IntVar()
        self.position_in = Checkbutton(position_frame, text="Use position", variable=v)
        self.position_in.var = v
        self.position_in.pack(side=LEFT, padx=5, pady=5)

        return segmentation_frame

    def build_spm_frame(self):
        spm_frame = Frame(self, borderwidth=1, relief=tkinter.GROOVE)
        spm_frame.pack(fill=X)

        spm_label = Label(spm_frame, text="Color detection")
        spm_label.pack(side=LEFT, padx=5, pady=5)

        spm_model_path_frame = Frame(spm_frame)
        spm_model_path_frame.pack(fill=X)
        self.spm_model_path_in = Label(spm_model_path_frame, text=self.configuration.spm_model_path)
        self.spm_model_path_in.pack(fill=X, padx=5, expand=True)
        browse_model = Button(spm_model_path_frame,
                              text="Browse model",
                              command=lambda: self.browse_file(self.spm_model_path_in))
        browse_model.pack(side=LEFT, padx=5, pady=5)



    def browse_file(self, label):
        filename = filedialog.askopenfilename()
        label.config(text=filename)

    def start_experiment(self):
        RunExperiment(self.configuration).start()


class RunExperiment(threading.Thread):
    def __init__(self, configuration):
        threading.Thread.__init__(self)
        self.configuration = configuration

    def run(self):
        print("Started thread")
        logger = CompositeLogger([ConsoleLogger(), FileLogger(self.configuration.results_path + '/logs.txt')])
        evaluator = Evaluator(self.configuration, logger)
        evaluator.run_validation()

def main():
    root = Tk()
    #root.geometry("300x300+300+300")
    app = EvaluatorMenu()
    root.mainloop()


if __name__ == '__main__':
    main()