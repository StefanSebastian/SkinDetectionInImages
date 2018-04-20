from tkinter import filedialog
from tkinter.ttk import Frame, Label, Button

from application_gui.config_views.utils import FileUtils


class ResourcePathFrame(Frame):
    def __init__(self, parent, configuration):
        Frame.__init__(self, parent)
        self.configuration = configuration

        self.test_path_in = None
        self.test_path_in_res = configuration.test_path_in

        self.test_path_expected = None
        self.test_path_expected_res = configuration.test_path_expected

        self.results_path = None
        self.results_path_res = configuration.results_path

        self.logging_path = None
        self.logging_path_res = configuration.logging_path

        self.init_view()

    def init_view(self):
        self.test_path_in = Label(self,
                                  text=FileUtils.get_filename_from_path(self.configuration.test_path_in))
        self.test_path_in.grid(row=0, column=1)
        Button(self,
               text="Browse...",
               command=self.browse_test_path_in) \
            .grid(row=0, column=0)

        self.test_path_expected = Label(self,
                                        text=FileUtils.get_filename_from_path(
                                            self.configuration.test_path_expected))
        self.test_path_expected.grid(row=1, column=1)
        Button(self,
               text="Browse...",
               command=self.browse_test_path_expected) \
            .grid(row=1, column=0)

        self.results_path = Label(self,
                                  text=FileUtils.get_filename_from_path(
                                      self.configuration.results_path))
        self.results_path.grid(row=2, column=1)
        Button(self,
               text="Browse...",
               command=self.browse_results_path) \
            .grid(row=2, column=0)

        self.logging_path = Label(self,
                                  text=FileUtils.get_filename_from_path(
                                      self.configuration.logging_path))
        self.logging_path.grid(row=3, column=1)
        Button(self,
               text="Browse...",
               command=self.browse_logging_path) \
            .grid(row=3, column=0)

    def browse_test_path_in(self):
        self.test_path_in_res = filedialog.askopenfilename()
        self.test_path_in.config(
            text=FileUtils.get_filename_from_path(self.test_path_in_res))

    def browse_test_path_expected(self):
        self.test_path_expected_res = filedialog.askopenfilename()
        self.test_path_expected.config(
            text=FileUtils.get_filename_from_path(self.test_path_expected_res))

    def browse_results_path(self):
        self.results_path_res = filedialog.askopenfilename()
        self.results_path.config(
            text=FileUtils.get_filename_from_path(self.results_path_res))

    def browse_logging_path(self):
        self.logging_path_res = filedialog.askopenfilename()
        self.logging_path.config(
            text=FileUtils.get_filename_from_path(self.logging_path_res))

    def get_values(self):
        return self.test_path_in_res, \
               self.test_path_expected_res,\
               self.results_path_res,\
               self.logging_path_res
