from tkinter import IntVar, END
from tkinter.ttk import Frame, Label, Checkbutton, Entry

from application_gui.validation_exception import ValidationError


class SizeConfigFrame(Frame):
    def __init__(self, parent, configuration):
        Frame.__init__(self, parent)
        self.configuration = configuration

        self.use_resize_in = None
        self.resize_val = IntVar()

        self.width_in = None
        self.height_in = None

        self.init_view()

    def init_view(self):

        self.use_resize_in = Checkbutton(self, text="Resize image", variable=self.resize_val).grid(row=0, column=0, columnspan=2)

        Label(self, text="Width").grid(row=1, column=0, sticky="w")
        self.width_in = Entry(self)
        self.width_in.insert(END, self.configuration.size[1])
        self.width_in.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        Label(self, text="Height").grid(row=2, column=0, sticky="w")
        self.height_in = Entry(self)
        self.height_in.insert(END, self.configuration.size[0])
        self.height_in.grid(row=2, column=1, sticky="w", padx=5, pady=5)

    def get_values(self):
        errors = []
        try:
            height_value = int(self.height_in.get())
        except ValueError:
            errors.append("Invalid height value")

        try:
            width_value = int(self.width_in.get())
        except ValueError:
            errors.append("Invalid width value")

        if errors:
            raise ValidationError("Size validation error", errors)

        return self.resize_val.get(), height_value, width_value