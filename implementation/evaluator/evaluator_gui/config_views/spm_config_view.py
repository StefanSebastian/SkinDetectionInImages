from tkinter import Frame, Label, Button, Entry, END
from tkinter.ttk import Combobox

from evaluator.evaluator_gui.config_views.utils import browse_file


class SpmConfigFrame(Frame):
    def __init__(self, parent, configuration):
        Frame.__init__(self, parent)
        self.configuration = configuration

        self.spm_model_path_in = None
        self.spm_threshold_in = None
        self.spm_type_in = None
        self.spm_neighbour_area = None

        self.init_view()

    def init_view(self):
        Label(self, text="Color detection").grid(row=0, column=0, rowspan=2)

        self.spm_model_path_in = Label(self, text=self.configuration.spm_model_path)
        self.spm_model_path_in.grid(row=0, column=2)

        Button(self,
               text="Browse model",
               command=lambda: browse_file(self.spm_model_path_in)) \
            .grid(row=0, column=1)

        Label(self, text="Threshold").grid(row=1, column=1)
        self.spm_threshold_in = Entry(self)
        self.spm_threshold_in.insert(END, self.configuration.spm_threshold)
        self.spm_threshold_in.grid(row=1, column=2)

        Label(self, text="Type").grid(row=2, column=1)
        self.spm_type_in = Combobox(self, values=['Most intense in superpixel', 'Average on superpixel'])
        self.spm_type_in.grid(row=2, column=2)

