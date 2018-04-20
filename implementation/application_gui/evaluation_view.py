import threading
import time
from tkinter import END, HORIZONTAL, VERTICAL, Toplevel, DISABLED, NORMAL
from tkinter.ttk import Frame, Button, Label, Separator

from application_gui.config_views.resource_path_config_view import ResourcePathFrame
from application_gui.config_views.size_config_view import SizeConfigFrame
from application_gui.config_views.spm_config_view import SpmConfigFrame
from application_gui.config_views.texture_config_view import TextureConfigFrame
from application_gui.evaluation_feedback_view import EvaluationFeedbackFrame
from application_gui.validation_exception import ValidationError

from evaluator.run_configuration import RunConfiguration
from evaluator.simulation import Evaluator
from application_gui.config_views.segmentation_config_view import SegmentationConfigFrame
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
        self.feedback_frame = None

        # experiment controls
        self.start_experiment_button = None
        self.stop_experiment_button = None
        self.experiment_running = False

        # build UI
        self.init_ui()

    def init_ui(self):

        self.segmentation_config_frame = SegmentationConfigFrame(self, self.configuration)
        Label(self, text="Segmentation").grid(row=0, column=0, sticky="w")
        self.segmentation_config_frame.grid(row=0, column=1, sticky="w")

        Separator(self, orient=HORIZONTAL).grid(row=1, column=0, sticky="ew", columnspan=2)

        self.spm_config_frame = SpmConfigFrame(self, self.configuration)
        Label(self, text="Color detection").grid(row=2, column=0, sticky="w")
        self.spm_config_frame.grid(row=2, column=1, sticky="w")

        Separator(self, orient=HORIZONTAL).grid(row=3, column=0, sticky="ew", columnspan=2)

        self.texture_config_frame = TextureConfigFrame(self, self.configuration)
        Label(self, text="Texture detection").grid(row=4, column=0, sticky="w")
        self.texture_config_frame.grid(row=4, column=1, sticky="w")

        Separator(self, orient=HORIZONTAL).grid(row=5, column=0, sticky="ew", columnspan=2)

        self.size_config_frame = SizeConfigFrame(self, self.configuration)
        Label(self, text="Image size").grid(row=6, column=0, sticky="w")
        self.size_config_frame.grid(row=6, column=1, sticky="w")

        Separator(self, orient=HORIZONTAL).grid(row=7, column=0, sticky="ew", columnspan=2)

        self.resource_paths_frame = ResourcePathFrame(self, self.configuration)
        Label(self, text="Resources").grid(row=8, column=0, sticky="w")
        self.resource_paths_frame.grid(row=8, column=1, sticky="w")

        Separator(self, orient=VERTICAL).grid(row=0, column=2, sticky="ns", rowspan=9)

        self.start_experiment_button = Button(self, text="Start experiment", command=self.start_experiment)
        self.start_experiment_button.grid(row=0, column=3, rowspan=1)

        self.stop_experiment_button = Button(self, text="Stop experiment", command=self.stop_experiment, state=DISABLED)
        self.stop_experiment_button.grid(row=1, column=3, rowspan=1)

        self.feedback_frame = EvaluationFeedbackFrame(self, self.configuration)
        self.feedback_frame.grid(row=2, column=3, rowspan=7)

        self.grid()

    def set_experiment_running(self, value):
        self.experiment_running = value
        if value is True:
            self.start_experiment_button.config(state=DISABLED)
            self.stop_experiment_button.config(state=NORMAL)
        else:
            self.start_experiment_button.config(state=NORMAL)
            self.stop_experiment_button.config(state=DISABLED)

    def stop_experiment(self):
        self.set_experiment_running(False)

    def start_experiment(self):
        self.set_experiment_running(True)
        try:
            sigma, tau, w_pos = self.segmentation_config_frame.get_values()
            self.configuration.qs_sigma = sigma
            self.configuration.qs_tau = tau
            self.configuration.qs_with_position = w_pos

            spm_model, spm_threshold, spm_type, spm_area = self.spm_config_frame.get_values()
            self.configuration.spm_model_path = spm_model
            self.configuration.spm_threshold = spm_threshold
            self.configuration.spm_type = spm_type
            self.configuration.spm_neighbour_area = spm_area

            text_model, text_type, text_area = self.texture_config_frame.get_values()
            self.configuration.texture_model_path = text_model
            self.configuration.texture_detection_type = text_type
            self.configuration.texture_detection_area = text_area

            use_rs, height, width = self.size_config_frame.get_values()
            if use_rs == 1:
                self.configuration.size = (height, width)

            test_path_in, test_path_exp, test_path_res, test_path_log = self.resource_paths_frame.get_values()
            self.configuration.test_path_in = test_path_in
            self.configuration.test_path_expected = test_path_exp
            self.configuration.results_path = test_path_res
            self.configuration.test_path_logging = test_path_log

            RunExperiment(self.configuration).start()
            MonitorExperiment(self.configuration, self.feedback_frame).start()

        except ValidationError as e:
            self.show_popup(str(e), e.errors)
            self.set_experiment_running(False)

    def show_popup(self, message, errors):
        toplevel = Toplevel(self)
        Label(toplevel, text=message).pack()
        for error in errors:
            Label(toplevel, text=error).pack()


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
    def __init__(self, configuration, feedback_frame):
        threading.Thread.__init__(self)
        self.configuration = configuration
        self.output_text_widget = feedback_frame.output_text
        self.progress_bar_widget = feedback_frame.progress_bar
        self.progress_label_widget = feedback_frame.progress_label

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

