from tkinter.ttk import Frame, Label, Button

from evaluator.evaluator_gui.config_views.utils import browse_file, get_filename_from_path


class ResourcePathFrame(Frame):
    def __init__(self, parent, configuration):
        Frame.__init__(self, parent)
        self.configuration = configuration

        self.test_path_in = None
        self.test_path_expected = None
        self.results_path = None
        self.logging_path = None

        self.init_view()

    def init_view(self):
        self.test_path_in = Label(self, text=get_filename_from_path(self.configuration.test_path_in))
        self.test_path_in.grid(row=0, column=1)
        Button(self,
               text="Browse...",
               command=lambda: browse_file(self.test_path_in)) \
            .grid(row=0, column=0)

        self.test_path_expected = Label(self, text=get_filename_from_path(self.configuration.test_path_expected))
        self.test_path_expected.grid(row=1, column=1)
        Button(self,
               text="Browse...",
               command=lambda: browse_file(self.test_path_expected)) \
            .grid(row=1, column=0)

        self.results_path = Label(self, text=get_filename_from_path(self.configuration.results_path))
        self.results_path.grid(row=2, column=1)
        Button(self,
               text="Browse...",
               command=lambda: browse_file(self.results_path)) \
            .grid(row=2, column=0)

        self.logging_path = Label(self, text=get_filename_from_path(self.configuration.logging_path))
        self.logging_path.grid(row=3, column=1)
        Button(self,
               text="Browse...",
               command=lambda: browse_file(self.logging_path)) \
            .grid(row=3, column=0)
