import tkinter
from tkinter import Tk, Text, TOP, BOTH, X, N, LEFT, IntVar, W
from tkinter.ttk import Frame, Label, Entry, Checkbutton, Button, Separator
from tkinter import filedialog

from evaluator.evaluator_gui.config_views.segmentation_config_view import SegmentationConfigFrame
from evaluator.evaluator_gui.config_views.spm_config_view import SpmConfigFrame
from evaluator.run_configuration import RunConfiguration
from evaluator.simulation import Evaluator

import threading

from utils.log import CompositeLogger, ConsoleLogger, FileLogger


class EvaluationFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent)

        # configuration for current experiment
        self.configuration = RunConfiguration()

        # all input widgets
        self.segmentation_config_frame = None
        self.spm_config_frame = None

        self.spm_model_path_in = None
        self.spm_threshold_in = None
        self.spm_type_in = None
        self.spm_neighbour_area_in = None

        # build UI
        self.init_ui()

    def init_ui(self):
        self.segmentation_config_frame = SegmentationConfigFrame(self, self.configuration)
        self.segmentation_config_frame.grid(row=0, column=0)

        self.spm_config_frame = SpmConfigFrame(self, self.configuration)
        self.spm_config_frame.grid(row=1, column=0)

        self.grid()

    '''
        Button(self.master, text="Start experiment", command=self.start_experiment).grid(row=4,column=0)
        Button(self.master, text="Display params", command=self.display_params).grid(row=4,column=1)
        '''

    def display_params(self):
        print(self.sigma_in)
        print(self.tau_in)
        print(self.position_in)

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