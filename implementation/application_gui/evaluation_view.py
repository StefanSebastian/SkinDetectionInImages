from tkinter import HORIZONTAL, VERTICAL
from tkinter.ttk import Frame, Label, Separator

from application_gui.config_views.resource_path_config_view import ResourcePathFrame
from application_gui.config_views.segmentation_config_view import SegmentationConfigFrame
from application_gui.config_views.size_config_view import SizeConfigFrame
from application_gui.config_views.spm_config_view import SpmConfigFrame
from application_gui.config_views.texture_config_view import TextureConfigFrame
from application_gui.process.feedback_view import FeedbackFrame
from application_gui.process.process_control_view import ProcessControlFrame
from evaluator.run_configuration import RunConfiguration
from evaluator.simulation import Evaluator


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

        self.experiment_controls_frame = ProcessControlFrame(self, self.config_extractor, EvaluationFrame.task_starter)
        self.experiment_controls_frame.grid(row=0, column=3, rowspan=9)

        self.grid()

    @staticmethod
    def task_starter(config, logger):
        evaluator = Evaluator(config, logger)
        evaluator.run_validation()

    def config_extractor(self):
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

        return self.configuration
