from tkinter.ttk import Frame

from application_gui.config_views.train_spm_config_view import TrainSpmConfigFrame
from color_analysis.train.train_config import SpmTrainConfiguration


class TrainSpmFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent)

        # configuration for training
        self.configuration = SpmTrainConfiguration()

        # input frame
        self.config_frame = None

        # feedback frame
        self.feedback_frame = None

        self.init_ui()

    def init_ui(self):
        self.config_frame = TrainSpmConfigFrame(self, self.configuration)
        self.config_frame.grid(row=0, column=0, sticky="w")

        self.grid()

