import multiprocessing
import threading
from multiprocessing import Queue
from tkinter import END, HORIZONTAL, VERTICAL, Toplevel, DISABLED, NORMAL
from tkinter.ttk import Frame, Button, Label, Separator

from application_gui.config_views.resource_path_config_view import ResourcePathFrame
from application_gui.config_views.segmentation_config_view import SegmentationConfigFrame
from application_gui.config_views.size_config_view import SizeConfigFrame
from application_gui.config_views.spm_config_view import SpmConfigFrame
from application_gui.config_views.texture_config_view import TextureConfigFrame
from application_gui.process.feedback_view import FeedbackFrame
from application_gui.process.monitoring import MonitorThread
from application_gui.process.process_control_view import ProcessControlFrame
from application_gui.util_views.popups import Popups
from application_gui.validation_exception import ValidationError
from evaluator.run_configuration import RunConfiguration
from evaluator.simulation import Evaluator
from utils.log import CompositeLogger, ConsoleLogger, QueueLogger


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
        self.experiment_controls_frame = None
        self.experiment_process = None
        self.monitor_thread = None

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

        self.experiment_controls_frame = ProcessControlFrame(self, self.start_experiment, self.stop_experiment)
        self.experiment_controls_frame.grid(row=0, column=3, rowspan=2)

        self.feedback_frame = FeedbackFrame(self)
        self.feedback_frame.grid(row=2, column=3, rowspan=7)

        self.grid()

    def stop_experiment(self):
        self.experiment_controls_frame.set_experiment_running(False)
        if self.experiment_process is not None:
            self.experiment_process.terminate()
            self.experiment_process.join()
            self.monitor_thread.set_running(False)

    def start_experiment(self):
        self.feedback_frame.reset()
        self.experiment_controls_frame.set_experiment_running(True)
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

            # start experiment
            process_queue = Queue()
            self.experiment_process = RunExperiment(self.configuration, process_queue)
            self.experiment_process.daemon = True
            self.experiment_process.start()

            self.monitor_thread = MonitorThread(self.feedback_frame, process_queue)
            self.monitor_thread.start()

        except ValidationError as e:
            Popups.show_error_popup(self, str(e), e.errors)
            self.experiment_controls_frame.set_experiment_running(False)


class RunExperiment(multiprocessing.Process):
    def __init__(self, configuration, process_queue):
        super(RunExperiment, self).__init__()
        self.configuration = configuration
        self.process_queue = process_queue

    def run(self):
        print("Started thread")
        logger = CompositeLogger([ConsoleLogger(), QueueLogger(self.process_queue)])
        evaluator = Evaluator(self.configuration, logger)
        evaluator.run_validation()



