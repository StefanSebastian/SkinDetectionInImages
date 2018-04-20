from tkinter import Frame, Label, Button, Entry, END
from tkinter import filedialog
from tkinter.ttk import Combobox

from evaluator.evaluator_gui.config_views.utils import browse_file, get_filename_from_path
from evaluator.evaluator_gui.validation_exception import ValidationError


class SpmConfigFrame(Frame):
    def __init__(self, parent, configuration):
        Frame.__init__(self, parent)
        self.configuration = configuration

        self.spm_model_path_in = None
        self.spm_model_path_res = configuration.spm_model_path

        self.spm_threshold_in = None

        self.spm_type_in = None
        self.spm_types = {'Most intense in superpixel' : 1, 'Average on superpixel' : 2}

        self.spm_neighbour_area_in = None

        self.init_view()

    def init_view(self):

        self.spm_model_path_in = Label(self, text=get_filename_from_path(self.configuration.spm_model_path))
        self.spm_model_path_in.grid(row=0, column=1)

        Button(self,
               text="Browse model",
               command=self.browse_spm_model) \
            .grid(row=0, column=0, sticky="w")

        Label(self, text="Threshold").grid(row=1, column=0, sticky="w")
        self.spm_threshold_in = Entry(self)
        self.spm_threshold_in.insert(END, self.configuration.spm_threshold)
        self.spm_threshold_in.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        Label(self, text="Type").grid(row=2, column=0, sticky="w")
        self.spm_type_in = Combobox(self, values=list(self.spm_types.keys()))
        self.spm_type_in.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        Label(self, text="Neighbour area").grid(row=3, column=0, sticky="w")
        self.spm_neighbour_area_in = Entry(self)
        self.spm_neighbour_area_in.insert(END, self.configuration.spm_neighbour_area)
        self.spm_neighbour_area_in.grid(row=3, column=1, sticky="w", padx=5, pady=5)

    def browse_spm_model(self):
        self.spm_model_path_res = filedialog.askopenfilename()
        self.spm_model_path_in.config(text=self.spm_model_path_res.split('/')[-1])

    def get_values(self):
        errors = []
        try:
            threshold_value = float(self.spm_threshold_in.get())
        except ValueError:
            errors.append("Invalid threshold value")

        if self.spm_type_in.get() not in self.spm_types:
            errors.append("You must select a spm type")

        try:
            neighbour_area_value = int(self.spm_neighbour_area_in.get())
        except ValueError:
            errors.append("Invalid value for spm neighbour area")

        if errors:
            raise ValidationError("SPM validation error", errors)
        return self.spm_model_path_res, threshold_value, self.spm_types[self.spm_type_in.get()], neighbour_area_value


