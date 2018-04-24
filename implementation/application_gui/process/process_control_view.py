from multiprocessing import Queue
import multiprocessing
from tkinter import DISABLED, NORMAL
from tkinter.ttk import Frame, Button

from application_gui.process.feedback_view import FeedbackFrame
from application_gui.process.monitoring import MonitorThread
from application_gui.util_views.popups import Popups
from application_gui.validation_exception import ValidationError
from utils.log import CompositeLogger, ConsoleLogger, QueueLogger


class ProcessControlFrame(Frame):
    """
    Controls a task (detection, evaluation, etc)

    has a frame for feedback, buttons to start and stop the task
    creates a separate process for the task and a monitor thread
    binds them with a Queue

    monitor thread displays messages in feedback frame
    """

    def __init__(self, parent, config_extractor, task_starter, before_hook=None, after_hook=None):
        Frame.__init__(self, parent)

        self.feedback_frame = None

        # experiment controls
        self.start_experiment_button = None
        self.stop_experiment_button = None
        self.experiment_running = False

        # extracts a configuration object
        self.config_extractor = config_extractor
        # takes a config and a logger and starts a task
        self.task_start = task_starter

        # process
        self.experiment_process = None
        # monitor thread
        self.monitor_thread = None

        # optional hooks before/after process
        self.before_hook = before_hook
        self.after_hook = after_hook

        self.init_view()

    def init_view(self):
        self.start_experiment_button = Button(self, text="Start experiment", command=self.start_process)
        self.start_experiment_button.grid(row=0, column=0)

        self.stop_experiment_button = Button(self, text="Stop experiment", command=self.stop_process, state=DISABLED)
        self.stop_experiment_button.grid(row=1, column=0)

        self.feedback_frame = FeedbackFrame(self)
        self.feedback_frame.grid(row=2, column=0)

    def set_experiment_running(self, value):
        self.experiment_running = value
        if value is True:
            self.start_experiment_button.config(state=DISABLED)
            self.stop_experiment_button.config(state=NORMAL)
        else:
            self.start_experiment_button.config(state=NORMAL)
            self.stop_experiment_button.config(state=DISABLED)

    def start_process(self):
        self.feedback_frame.reset()
        self.set_experiment_running(True)
        try:
            configuration = self.config_extractor()

            # optional operations before starting process
            if self.before_hook:
                self.before_hook(configuration)

            # start experiment
            process_queue = Queue()
            self.experiment_process = RunExperiment(configuration, process_queue, self.task_start)
            self.experiment_process.daemon = True
            self.experiment_process.start()

            self.monitor_thread = MonitorThread(self.feedback_frame, process_queue)
            self.monitor_thread.start()

        except ValidationError as e:
            Popups.show_error_popup(self, str(e), e.errors)
            self.set_experiment_running(False)

    def stop_process(self):
        self.set_experiment_running(False)
        if self.experiment_process is not None:
            self.experiment_process.terminate()
            self.experiment_process.join()
            self.monitor_thread.set_running(False)


class RunExperiment(multiprocessing.Process):
    def __init__(self, configuration, process_queue, task_starter):
        super(RunExperiment, self).__init__()
        self.configuration = configuration
        self.process_queue = process_queue
        self.task_starter = task_starter

    def run(self):
        print("Started thread")
        logger = CompositeLogger([ConsoleLogger(), QueueLogger(self.process_queue)])
        self.task_starter(self.configuration, logger)
