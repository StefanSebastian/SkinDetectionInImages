from tkinter.ttk import Frame, Label, Checkbutton, Entry
from tkinter import IntVar


class SegmentationConfigFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent)

        self.sigma_in = None
        self.tau_in = None
        self.position_in = None

        self.init_view()

    def init_view(self):
        Label(self, text="Segmentation").grid(row=0, column=0, rowspan=3)
        Label(self, text="Sigma").grid(row=0, column=1)
        self.sigma_in = Entry(self).grid(row=0, column=2)

        Label(self, text="Tau").grid(row=1, column=1)
        self.tau_in = Entry(self).grid(row=1, column=2)

        value = IntVar
        self.position_in = Checkbutton(self, text="Use position", variable=value).grid(row=2, column=1, columnspan=2)
        self.position_in = value
