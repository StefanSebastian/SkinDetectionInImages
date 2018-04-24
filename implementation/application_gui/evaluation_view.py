from tkinter.ttk import Frame

from application_gui.config_views.detection_config_group import DetectionConfigFrame
from application_gui.process.process_control_view import ProcessControlFrame
from evaluator.run_configuration import RunConfiguration
from evaluator.simulation import Evaluator


class EvaluationFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        # configuration for current experiment
        self.configuration = RunConfiguration()

        # all input widgets
        self.config_frame = None

        # output widgets
        self.experiment_controls_frame = None

        # build UI
        self.init_ui()

    def init_ui(self):
        self.config_frame = DetectionConfigFrame(self, self.configuration)
        self.config_frame.grid(row=0, column=0)

        self.experiment_controls_frame = ProcessControlFrame(self, self.config_extractor, EvaluationFrame.task_starter)
        self.experiment_controls_frame.grid(row=0, column=1)

        self.grid()

    @staticmethod
    def task_starter(config, logger):
        evaluator = Evaluator(config, logger)
        evaluator.run_validation()

    def config_extractor(self):
        return self.config_frame.get_config()
