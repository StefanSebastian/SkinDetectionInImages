import threading
from tkinter import Text, END, INSERT
from tkinter.ttk import Frame, Button
import time

from evaluator.evaluator_gui.config_views.segmentation_config_view import SegmentationConfigFrame
from evaluator.evaluator_gui.config_views.spm_config_view import SpmConfigFrame
from evaluator.run_configuration import RunConfiguration
from evaluator.simulation import Evaluator
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

        # output widgets
        self.output_text = None

        # build UI
        self.init_ui()

    def init_ui(self):
        self.segmentation_config_frame = SegmentationConfigFrame(self, self.configuration)
        self.segmentation_config_frame.grid(row=0, column=0)

        self.spm_config_frame = SpmConfigFrame(self, self.configuration)
        self.spm_config_frame.grid(row=1, column=0)

        Button(self, text="Start experiment", command=self.start_experiment).grid(row=2, column=0)

        self.output_text = Text(self, height=10)
        self.output_text.grid(row=3, column=0)

        self.grid()

    def start_experiment(self):
        RunExperiment(self.configuration).start()
        MonitorExperiment(self.configuration, self.output_text).start()


class RunExperiment(threading.Thread):
    def __init__(self, configuration):
        threading.Thread.__init__(self)
        self.configuration = configuration

    def run(self):
        print("Started thread")
        logger = CompositeLogger([ConsoleLogger(), FileLogger(self.configuration.logging_path)])
        evaluator = Evaluator(self.configuration, logger)
        evaluator.run_validation()


class MonitorExperiment(threading.Thread):
    def __init__(self, configuration, output_text_widget):
        threading.Thread.__init__(self)
        self.configuration = configuration
        self.output_text_widget = output_text_widget

        open(self.configuration.logging_path, 'w').close() # clear logs

    def run(self):
        while True:
            time.sleep(1)
            f = open(self.configuration.logging_path, "r")
            text = f.read()
            self.output_text_widget.insert(END, text)
            self.output_text_widget.see(END)

