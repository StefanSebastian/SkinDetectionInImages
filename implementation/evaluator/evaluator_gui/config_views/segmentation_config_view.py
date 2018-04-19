from tkinter.ttk import Frame, Label, Checkbutton, Entry
from tkinter import IntVar, END


class SegmentationConfigFrame(Frame):
    def __init__(self, parent, configuration):
        Frame.__init__(self, parent)
        self.configuration = configuration

        self.sigma_in = None
        self.tau_in = None
        self.position_in = None

        self.init_view()

    def init_view(self):
        Label(self, text="Sigma").grid(row=0, column=0, sticky="w")
        self.sigma_in = Entry(self)
        self.sigma_in.insert(END, self.configuration.qs_sigma)
        self.sigma_in.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        Label(self, text="Tau").grid(row=1, column=0, sticky="w")
        self.tau_in = Entry(self)
        self.tau_in.insert(END, self.configuration.qs_tau)
        self.tau_in.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        value = IntVar()
        self.position_in = Checkbutton(self, text="Use position", variable=value)\
            .grid(row=2, column=0, columnspan=2, sticky="w", padx=5, pady=5)
