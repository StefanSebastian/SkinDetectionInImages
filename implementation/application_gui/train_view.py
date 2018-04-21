from tkinter.ttk import Frame
import multiprocessing
from multiprocessing import Queue

from application_gui.config_views.train_spm_config_view import TrainSpmConfigFrame
from application_gui.process.feedback_view import FeedbackFrame
from application_gui.process.monitoring import MonitorThread
from application_gui.process.process_control_view import ProcessControlFrame
from application_gui.util_views.popups import Popups
from application_gui.validation_exception import ValidationError
from color_analysis.train.train_config import SpmTrainConfiguration
from color_analysis.train.trainer import SPMModelTrainer
from utils.log import CompositeLogger, ConsoleLogger, QueueLogger


class TrainSpmFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent)

        # configuration for training
        self.configuration = SpmTrainConfiguration()

        # input frame
        self.config_frame = None

        # feedback frame
        self.feedback_frame = None
        self.train_control_frame = None

        self.train_process = None
        self.monitor_thread = None

        self.init_ui()

    def init_ui(self):
        self.config_frame = TrainSpmConfigFrame(self, self.configuration)
        self.config_frame.grid(row=0, column=0, sticky="w")

        self.train_control_frame = ProcessControlFrame(self, self.start_training, self.stop_training)
        self.train_control_frame.grid(row=0, column=1, sticky="ew")

        self.feedback_frame = FeedbackFrame(self)
        self.feedback_frame.grid(row=1, column=1, sticky="ew")

        self.grid()

    def start_training(self):
        self.feedback_frame.reset()
        self.train_control_frame.set_experiment_running(True)
        try:
            # start experiment
            process_queue = Queue()
            self.train_process = RunTraining(self.configuration, process_queue)
            self.train_process.daemon = True
            self.train_process.start()

            self.monitor_thread = MonitorThread(self.feedback_frame, process_queue)
            self.monitor_thread.start()

        except ValidationError as e:
            Popups.show_error_popup(self, str(e), e.errors)
            self.train_control_frame.set_experiment_running(False)

    def stop_training(self):
        self.train_control_frame.set_experiment_running(False)
        if self.train_process is not None:
            self.train_process.terminate()
            self.train_process.join()
            self.monitor_thread.set_running(False)


class RunTraining(multiprocessing.Process):
    def __init__(self, configuration, process_queue):
        super(RunTraining, self).__init__()
        self.configuration = configuration
        self.process_queue = process_queue

    def run(self):
        print("Started thread")
        logger = CompositeLogger([ConsoleLogger(), QueueLogger(self.process_queue)])
        SPMModelTrainer.train_spm_model(self.configuration, logger)
