from utils.general import print_progress
from utils.general import print_progress_pixel

message_process_done = "Process finished"
progress_prefix = "Progress:"


class ConsoleLogger:
    def log(self, message):
        print(message)

    def log_progress(self, pos, total):
        print_progress(pos, total)

    def log_progress_pixel(self, x_pixel, y_pixel, rows, cols):
        print_progress_pixel(x_pixel, y_pixel, rows, cols)

    def log_done(self):
        print(message_process_done)


class FileLogger:
    def __init__(self, path):
        self.path = path

    def log(self, message):
        with open(self.path, 'a') as log_file:
            log_file.write(message + '\n')

    def log_progress(self, pos, total):
        self.log(progress_prefix + str((pos/total) * 100))

    def log_progress_pixel(self, x_pixel, y_pixel, rows, cols):
        pos = x_pixel * cols + y_pixel
        if pos % 300 == 0:
            prog = pos / (rows * cols)
            self.log(progress_prefix + str(prog * 100))

    def log_done(self):
        self.log(message_process_done)


class QueueLogger:
    def __init__(self, queue):
        self.queue = queue

    def log(self, message):
        self.queue.put(message + '\n')

    def log_progress(self, pos, total):
        self.log(progress_prefix + str((pos/total) * 100))

    def log_progress_pixel(self, x_pixel, y_pixel, rows, cols):
        pos = x_pixel * cols + y_pixel
        if pos % 300 == 0:
            prog = pos / (rows * cols)
            self.log(progress_prefix + str(prog * 100))

    def log_done(self):
        self.log(message_process_done)


class CompositeLogger:
    def __init__(self, loggers):
        self.loggers = loggers

    def log(self, message):
        for logger in self.loggers:
            logger.log(message)

    def log_progress(self, pos, total):
        for logger in self.loggers:
            logger.log_progress(pos, total)

    def log_progress_pixel(self, x_pixel, y_pixel, rows, cols):
        for logger in self.loggers:
            logger.log_progress_pixel(x_pixel, y_pixel, rows, cols)

    def log_done(self):
        for logger in self.loggers:
            logger.log_done()


class LogFactory:
    @staticmethod
    def get_default_logger():
        return CompositeLogger([ConsoleLogger(), FileLogger('logs.txt')])
