from tkinter import END
from tkinter.ttk import Combobox, Entry, Frame, Label, Button

from evaluator.evaluator_gui.config_views.utils import browse_file


class TextureConfigFrame(Frame):
    def __init__(self, parent, configuration):
        Frame.__init__(self, parent)
        self.configuration = configuration

        self.texture_model_path_in = None
        self.texture_detection_type_in = None
        self.texture_detection_area_in = None

        self.init_view()

    def init_view(self):
        Label(self, text="Texture detection").grid(row=0, column=0, rowspan=3)

        self.texture_model_path_in = Label(self, text=self.configuration.texture_model_path)
        self.texture_model_path_in.grid(row=0, column=2)

        Button(self,
               text="Browse model",
               command=lambda: browse_file(self.texture_model_path_in))\
            .grid(row=0, column=1)

        Label(self, text="Detection type").grid(row=1, column=1)
        self.texture_detection_type_in = Combobox(self, values=['Window scan', 'Around each pixel'])
        self.texture_detection_type_in.grid(row=1, column=2)

        Label(self, text="Detection area").grid(row=2, column=1)
        self.texture_detection_area_in = Entry(self)
        self.texture_detection_area_in.insert(END, self.configuration.texture_detection_area)
        self.texture_detection_area_in.grid(row=2, column=2)


