from tkinter.ttk import Frame

from application_gui.config_views.detection_config_group import DetectionConfigFrame
from application_gui.image_display_view import ImageDisplayFrame
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

        # image
        self.image_display_frame = None

        self.init_ui()

    def init_ui(self):
        self.config_frame = DetectionConfigFrame(self, self.configuration)
        self.config_frame.grid(row=0, column=0)

        self.process_frame = ProcessControlFrame(self, self.config_extractor, self.task_starter, self.before_start, self.on_finish)
        self.process_frame.grid(row=0, column=1)

        self.image_display_frame = ImageDisplayFrame(self)
        self.image_display_frame.grid(row=0, column=2)

        self.grid()

    def config_extractor(self):
        return self.config_frame.get_config()

    @staticmethod
    def task_starter(config, logger):
        evaluator = Evaluator(config, logger)
        evaluator.run_detection()

    def before_start(self, configuration):
        self.image_display_frame.set_input_image(configuration.detection_path)

    def on_finish(self, configuration):
        self.image_display_frame.set_output_image(configuration.results_path + '/' +
                                                  configuration.detection_result_image_name)
