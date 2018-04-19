from tkinter.ttk import Frame, Progressbar, Label
from tkinter import Text


class EvaluationFeedbackFrame(Frame):

    def __init__(self, parent, configuration):
        Frame.__init__(self, parent)
        self.configuration = configuration

        self.output_text = None
        self.progress_bar = None
        self.progress_label = None

        self.init_view()

    def init_view(self):
        self.output_text = Text(self, height=10)
        self.output_text.grid(row=0, column=0)
        self.progress_bar = Progressbar(self, orient='horizontal')
        self.progress_bar['maximum'] = 100
        self.progress_bar.grid(row=1, column=0)
        self.progress_label = Label(self)
        self.progress_label.grid(row=2, column=0)

