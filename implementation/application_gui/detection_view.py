from tkinter.ttk import Frame

from application_gui.config_views.detection_config_group import DetectionConfigFrame
from application_gui.process.process_control_view import ProcessControlFrame
from evaluator.run_configuration import RunConfiguration
from evaluator.simulation import Evaluator


class DetectionFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        # run configuration and frame
        self.configuration = RunConfiguration()
        self.config_frame = None

        # feedback frame
        self.process_frame = None

        self.init_ui()

    def init_ui(self):
        self.config_frame = DetectionConfigFrame(self, self.configuration)
        self.config_frame.grid(row=0, column=0)

        self.process_frame = ProcessControlFrame(self, self.config_extractor, DetectionFrame.task_starter)
        self.process_frame.grid(row=0, column=1)

        self.grid()

    def config_extractor(self):
        return self.config_frame.get_config()

    @staticmethod
    def task_starter(config, logger):
        evaluator = Evaluator(config, logger)
        evaluator.run_detection()
