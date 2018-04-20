from tkinter import END
from tkinter import filedialog
from tkinter.ttk import Combobox, Entry, Frame, Label, Button

from application_gui.validation_exception import ValidationError

from application_gui.config_views.utils import FileUtils


class TextureConfigFrame(Frame):
    def __init__(self, parent, configuration):
        Frame.__init__(self, parent)
        self.configuration = configuration

        self.texture_model_path_in = None
        self.texture_model_path_res = configuration.texture_model_path

        self.texture_detection_type_in = None
        self.texture_types = {'Window scan': 0, 'Around each pixel': 1}

        self.texture_detection_area_in = None

        self.init_view()

    def init_view(self):

        self.texture_model_path_in = Label(self,
                                           text=FileUtils.get_filename_from_path(self.configuration.texture_model_path))
        self.texture_model_path_in.grid(row=0, column=1, sticky="we", padx=5, pady=5)

        Button(self,
               text="Browse model",
               command=self.browse_texture_model)\
            .grid(row=0, column=0, sticky="w")

        Label(self, text="Detection type").grid(row=1, column=0, sticky="w")
        self.texture_detection_type_in = Combobox(self, values=list(self.texture_types.keys()))
        self.texture_detection_type_in.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        Label(self, text="Detection area").grid(row=2, column=0, sticky="w")
        self.texture_detection_area_in = Entry(self)
        self.texture_detection_area_in.insert(END, self.configuration.texture_detection_area)
        self.texture_detection_area_in.grid(row=2, column=1, sticky="w", padx=5, pady=5)

    def get_values(self):
        errors = []
        try:
            texture_area_value = int(self.texture_detection_area_in.get())
        except ValueError:
            errors.append("Invalid texture area")

        if self.texture_detection_type_in.get() not in self.texture_types:
            errors.append("You must select a texture detection type")

        if errors:
            raise ValidationError("Texture validation error", errors)

        return self.texture_model_path_res, self.texture_types[self.texture_detection_type_in.get()], texture_area_value

    def browse_texture_model(self):
        self.texture_model_path_res = filedialog.askopenfilename()
        self.texture_model_path_in.config(text=self.texture_model_path_res.split('/')[-1])
