import threading
from tkinter import END

from utils import log


class MonitorThread(threading.Thread):
    def __init__(self, feedback_frame, process_queue, process_finished_callback):
        threading.Thread.__init__(self)
        self.output_text_widget = feedback_frame.output_text
        self.progress_bar_widget = feedback_frame.progress_bar
        self.progress_label_widget = feedback_frame.progress_label

        self.process_queue = process_queue
        self.running = True

        self.process_finished_callback = process_finished_callback

    def set_running(self, running):
        self.running = running

    def run(self):
        while self.running:
            line = self.process_queue.get()
            if log.progress_prefix in line:
                value_str = line.split(':')[1]
                value = int(float(value_str))
                self.progress_bar_widget["value"] = value
            else:
                self.output_text_widget.insert(END, line)
                self.output_text_widget.see(END)
                self.progress_label_widget['text'] = line

                if log.message_process_done in line:
                    self.process_finished_callback()
