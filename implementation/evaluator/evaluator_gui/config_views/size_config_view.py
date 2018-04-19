from tkinter import IntVar, END
from tkinter.ttk import Frame, Label, Checkbutton, Entry


class SizeConfigFrame(Frame):
    def __init__(self, parent, configuration):
        Frame.__init__(self, parent)
        self.configuration = configuration

        self.use_resize_in = None
        self.width_in = None
        self.height_in = None

        self.init_view()

    def init_view(self):
        Label(self, text="Image size").grid(row=0, column=0, rowspan=2)

        value = IntVar()
        self.use_resize_in = Checkbutton(self, text="Use position", variable=value).grid(row=0, column=1, columnspan=2)

        Label(self, text="Width").grid(row=1, column=1)
        self.width_in = Entry(self)
        self.width_in.insert(END, self.configuration.size[1])
        self.width_in.grid(row=1, column=2)

        Label(self, text="Height").grid(row=2, column=1)
        self.height_in = Entry(self)
        self.height_in.insert(END, self.configuration.size[0])
        self.height_in.grid(row=2, column=2)
