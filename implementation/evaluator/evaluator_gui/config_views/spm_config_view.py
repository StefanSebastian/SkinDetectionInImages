from tkinter import Frame, Label, Button


class SpmConfigFrame(Frame):
    def __init__(self, parent, configuration):
        Frame.__init__(self, parent)
        self.configuration = configuration

        self.spm_model_path_in = None

        self.init_view()

    def init_view(self):
        Label(self, text="Color detection").grid(row=0, column=0)
        Button(self,
               text="Browse model",
               command=lambda: self.browse_file(self.spm_model_path_in)) \
            .grid(row=0, column=1)
        self.spm_model_path_in = Label(self, text=self.configuration.spm_model_path) \
            .grid(row=0, column=2)
