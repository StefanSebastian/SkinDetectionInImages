from tkinter import filedialog, END
from tkinter.ttk import Frame, Label, Button, Entry

from application_gui.config_views.utils import FileUtils
from application_gui.validation_exception import ValidationError


class TrainTextureConfigFrame(Frame):
    def __init__(self, parent, configuration):
        Frame.__init__(self, parent)

        self.configuration = configuration

        self.path_positive_res = configuration.path_pos
        self.path_positive_in = None

        self.path_negative_res = configuration.path_neg
        self.path_negative_in = None

        self.path_to_models = None
        self.path_to_models_res = configuration.path_models

        self.model_name = None

        self.init_ui()

    def init_ui(self):
        self.path_positive_in = Label(self,
                                     text=FileUtils.get_filename_from_path(self.configuration.path_pos))
        self.path_positive_in.grid(row=0, column=1)
        Button(self,
               text="Path to positive examples",
               command=self.browse_positive_path) \
            .grid(row=0, column=0, sticky="w")

        self.path_negative_in = Label(self,
                                       text=FileUtils.get_filename_from_path(self.configuration.path_neg))
        self.path_negative_in.grid(row=1, column=1)
        Button(self,
               text="Path to negative examples",
               command=self.browse_negative_path) \
            .grid(row=1, column=0, sticky="w")

        self.path_to_models = Label(self,
                                    text=FileUtils.get_filename_from_path(self.configuration.path_models))
        self.path_to_models.grid(row=2, column=1)
        Button(self,
               text="Folder to store model",
               command=self.browse_model_path).\
            grid(row=2, column=0, sticky="w")

        Label(self, text="Model name").grid(row=3, column=0, sticky="w")
        self.model_name = Entry(self)
        self.model_name.insert(END, self.configuration.selected_classifier)
        self.model_name.grid(row=3, column=1, sticky="w")

    def browse_positive_path(self):
        self.path_positive_res = filedialog.askdirectory()
        self.path_positive_in.config(text=self.path_positive_res.split('/')[-1])

    def browse_negative_path(self):
        self.path_negative_res = filedialog.askdirectory()
        self.path_negative_in.config(text=self.path_negative_res.split('/')[-1])

    def browse_model_path(self):
        self.path_to_models_res = filedialog.askdirectory()
        self.path_to_models.config(text=self.path_to_models_res.split('/')[-1])

    def get_values(self):
        errors = []

        if self.model_name.get() == "":
            errors.append("Invalid model name")

        if errors:
            raise ValidationError("SPM train config validation error", errors)

        return self.path_positive_res, self.path_negative_res, self.path_to_models_res, self.model_name.get()
