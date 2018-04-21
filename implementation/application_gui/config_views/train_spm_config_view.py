from tkinter.ttk import Frame, Label, Combobox


class TrainSpmConfigFrame(Frame):
    def __init__(self, parent, configuration):
        Frame.__init__(self, parent)

        self.configuration = configuration

        self.color_space = None
        self.color_spaces = ["RGB", "HSV", "YCrCb"]

        self.path_to_data = None
        self.path_to_models = None
        self.model_name = None

        self.init_ui()

    def init_ui(self):
        Label(self, text="Color space").grid(row=0, column=0, sticky="w")
        self.color_space = Combobox(self, values=self.color_spaces)
        self.color_space.grid(row=0, column=1, sticky="w", padx=5, pady=5)


