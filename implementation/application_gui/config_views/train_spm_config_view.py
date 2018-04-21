from tkinter import filedialog, END
from tkinter.ttk import Frame, Label, Combobox, Button, Entry

from application_gui.config_views.utils import FileUtils


class TrainSpmConfigFrame(Frame):
    def __init__(self, parent, configuration):
        Frame.__init__(self, parent)

        self.configuration = configuration

        self.color_space = None
        self.color_spaces = ["RGB", "HSV", "YCrCb"]

        self.path_to_data_res = None
        self.path_to_data_in = FileUtils.get_filename_from_path(configuration.path_compaq)

        self.path_to_models = None
        self.path_to_models_res = FileUtils.get_filename_from_path(configuration.path_models)

        self.model_name = None

        self.init_ui()

    def init_ui(self):
        Label(self, text="Color space").grid(row=0, column=0, sticky="w")
        self.color_space = Combobox(self, values=self.color_spaces)
        self.color_space.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        self.path_to_data_in = Label(self,
                                       text=FileUtils.get_filename_from_path(self.configuration.path_compaq))
        self.path_to_data_in.grid(row=1, column=1)
        Button(self,
               text="Path to input data",
               command=self.browse_input_data_path) \
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
        self.model_name.insert(END, self.configuration.selected_model)
        self.model_name.grid(row=3, column=1, sticky="w")

    def browse_input_data_path(self):
        self.path_to_data_res = filedialog.askdirectory()
        self.path_to_data_in.config(text=self.path_to_data_res.split('/')[-1])

    def browse_model_path(self):
        self.path_to_models_res = filedialog.askdirectory()
        self.path_to_models.config(text=self.path_to_models_res.split('/')[-1])
