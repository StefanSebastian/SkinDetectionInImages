from tkinter.ttk import Frame

from application_gui.config_views.train_spm_config_view import TrainSpmConfigFrame
from application_gui.process.process_control_view import ProcessControlFrame
from color_analysis.train.train_config import SpmTrainConfiguration
from color_analysis.train.trainer import SPMModelTrainer


class TrainSpmFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        # configuration for training
        self.configuration = SpmTrainConfiguration()

        # input frame
        self.config_frame = None

        # process frame
        self.train_control_frame = None

        self.init_ui()

    def init_ui(self):
        self.config_frame = TrainSpmConfigFrame(self, self.configuration)
        self.config_frame.grid(row=0, column=0, sticky="w")

        self.train_control_frame = ProcessControlFrame(self, self.config_extractor, TrainSpmFrame.task_starter)
        self.train_control_frame.grid(row=0, column=1, sticky="ew")

        self.grid()

    def config_extractor(self):
        color_space, data_path, res_path, model_nm = self.config_frame.get_values()
        self.configuration.color_space = color_space
        self.configuration.path_compaq = data_path
        self.configuration.path_models = res_path
        self.configuration.selected_model = model_nm
        return self.configuration

    @staticmethod
    def task_starter(configuration, logger):
        SPMModelTrainer.train_spm_model(configuration, logger)
