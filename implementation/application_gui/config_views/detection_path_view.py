from tkinter import filedialog
from tkinter.ttk import Frame, Label, Button

from application_gui.config_views.utils import FileUtils


class DetectionPathFrame(Frame):
    def __init__(self, parent, configuration):
        Frame.__init__(self, parent)
        self.configuration = configuration

        self.detection_path = None
        self.detection_path_res = configuration.detection_path

        self.results_path = None
        self.results_path_res = configuration.results_path

        self.init_ui()

    def init_ui(self):
        self.detection_path = Label(self,
                                  text=FileUtils.get_filename_from_path(self.configuration.detection_path))
        self.detection_path.grid(row=0, column=1)
        Button(self,
               text="Input image",
               command=self.browse_image_path) \
            .grid(row=0, column=0)

        self.results_path = Label(self,
                                    text=FileUtils.get_filename_from_path(self.configuration.results_path))
        self.results_path.grid(row=1, column=1)
        Button(self,
               text="Result path",
               command=self.browse_results_path) \
            .grid(row=1, column=0)

    def browse_image_path(self):
        self.detection_path_res = filedialog.askopenfilename()
        self.detection_path.config(
            text=FileUtils.get_filename_from_path(self.detection_path_res))

    def browse_results_path(self):
        self.results_path_res = filedialog.askdirectory()
        self.results_path.config(
            text=FileUtils.get_filename_from_path(self.results_path_res)
        )

    def get_values(self):
        return self.detection_path_res, self.results_path_res
