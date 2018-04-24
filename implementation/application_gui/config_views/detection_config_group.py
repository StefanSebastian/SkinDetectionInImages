from tkinter import HORIZONTAL, VERTICAL
from tkinter.ttk import Frame, Label, Separator

from application_gui.config_views.detection_path_view import DetectionPathFrame
from application_gui.config_views.resource_path_config_view import ResourcePathFrame
from application_gui.config_views.segmentation_config_view import SegmentationConfigFrame
from application_gui.config_views.size_config_view import SizeConfigFrame
from application_gui.config_views.spm_config_view import SpmConfigFrame
from application_gui.config_views.texture_config_view import TextureConfigFrame


class DetectionConfigFrame(Frame):
    def __init__(self, parent, configuration):
        Frame.__init__(self, parent)
        self.configuration = configuration

        self.segmentation_config_frame = None
        self.spm_config_frame = None
        self.texture_config_frame = None
        self.size_config_frame = None
        self.detection_path_frame = None

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

        self.detection_path_frame = DetectionPathFrame(self, self.configuration)
        Label(self, text="Input image").grid(row=8, column=0, sticky="w")
        self.detection_path_frame.grid(row=8, column=1, sticky="w")

        Separator(self, orient=VERTICAL).grid(row=0, column=2, sticky="ns", rowspan=9)

    def get_config(self):
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

        detection_path, results_path = self.detection_path_frame.get_values()
        self.configuration.detection_path = detection_path
        self.configuration.results_path = results_path

        return self.configuration
