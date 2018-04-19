import threading
from tkinter import Text, END, INSERT
from tkinter.ttk import Frame, Button, Progressbar, Label
import time

from evaluator.evaluator_gui.config_views.resource_path_config_view import ResourcePathFrame
from evaluator.evaluator_gui.config_views.segmentation_config_view import SegmentationConfigFrame
from evaluator.evaluator_gui.config_views.size_config_view import SizeConfigFrame
from evaluator.evaluator_gui.config_views.spm_config_view import SpmConfigFrame
from evaluator.evaluator_gui.config_views.texture_config_view import TextureConfigFrame
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
        self.texture_config_frame = None
        self.size_config_frame = None
        self.resource_paths_frame = None

        # output widgets
        self.output_text = None
        self.progress_bar = None
        self.progress_label = None

        # build UI
        self.init_ui()

    def init_ui(self):
        self.segmentation_config_frame = SegmentationConfigFrame(self, self.configuration)
        self.segmentation_config_frame.grid(row=0, column=0)

        self.spm_config_frame = SpmConfigFrame(self, self.configuration)
        self.spm_config_frame.grid(row=1, column=0)

        self.texture_config_frame = TextureConfigFrame(self, self.configuration)
        self.texture_config_frame.grid(row=2, column=0)

        self.size_config_frame = SizeConfigFrame(self, self.configuration)
        self.size_config_frame.grid(row=3, column=0)

        self.resource_paths_frame = ResourcePathFrame(self, self.configuration)
        self.resource_paths_frame.grid(row=4, column=0)

        Button(self, text="Start experiment", command=self.start_experiment).grid(row=5, column=0)
        self.output_text = Text(self, height=10)
        self.output_text.grid(row=6, column=0)
        self.progress_bar = Progressbar(self, orient='horizontal')
        self.progress_bar['maximum'] = 100
        self.progress_bar.grid(row=7, column=0)
        self.progress_label = Label(self)
        self.progress_label.grid(row=8, column=0)

        self.grid()

    def start_experiment(self):
        RunExperiment(self.configuration).start()
        MonitorExperiment(self.configuration, self.output_text, self.progress_bar, self.progress_label).start()


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
    def __init__(self, configuration, output_text_widget, progress_bar_widget, progress_label_widget):
        threading.Thread.__init__(self)
        self.configuration = configuration
        self.output_text_widget = output_text_widget
        self.progress_bar_widget = progress_bar_widget
        self.progress_label_widget = progress_label_widget

        open(self.configuration.logging_path, 'w').close() # clear logs

    def run(self):
        last_processed_line = 0
        while True:
            time.sleep(1)
            f = open(self.configuration.logging_path, "r")
            lines = f.readlines()

            if not lines:
                continue

            lines_size = len(lines)
            lines = lines[last_processed_line:]
            last_processed_line = lines_size
            for line in lines:
                if "Progress" in line:
                    value_str = line.split(':')[1]
                    value = int(float(value_str))
                    self.progress_bar_widget["value"] = value
                else:
                    self.output_text_widget.insert(END, line)
                    self.output_text_widget.see(END)
                    self.progress_label_widget['text'] = line

