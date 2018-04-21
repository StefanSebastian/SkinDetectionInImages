from tkinter.ttk import Frame

from application_gui.config_views.train_texture_config_view import TrainTextureConfigFrame
from application_gui.process.process_control_view import ProcessControlFrame
from texture_analysis.train.train_configuration import TextureTrainConfiguration
from texture_analysis.train.trainer import TextureModelTrainer


class TrainTextureFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        # configuration for training
        self.configuration = TextureTrainConfiguration()

        # input frame
        self.config_frame = None

        # process frame
        self.train_control_frame = None

        self.init_ui()

    def init_ui(self):
        self.config_frame = TrainTextureConfigFrame(self, self.configuration)
        self.config_frame.grid(row=0, column=0, sticky="w")

        self.train_control_frame = ProcessControlFrame(self, self.config_extractor, TrainTextureFrame.task_starter)
        self.train_control_frame.grid(row=0, column=1, sticky="ew")

        self.grid()

    def config_extractor(self):
        pos_pat, neg_path, res_path, model_nm = self.config_frame.get_values()
        self.configuration.path_pos = pos_pat
        self.configuration.path_neg = neg_path
        self.configuration.path_models = res_path
        self.configuration.selected_classifier = model_nm
        return self.configuration

    @staticmethod
    def task_starter(configuration, logger):
        TextureModelTrainer.train_model(configuration, logger)
