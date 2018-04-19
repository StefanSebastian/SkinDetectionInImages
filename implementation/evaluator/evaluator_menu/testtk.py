from tkinter import Tk, Text, TOP, BOTH, X, N, LEFT, IntVar
from tkinter.ttk import Frame, Label, Entry, Checkbutton, Button
from evaluator.simulation import Evaluator

import threading


class Example(Frame):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.master.title("Review")
        self.pack(fill=BOTH, expand=True)

        segmentation_frame = self.build_segmentation_frame()

        start_experiment_button = Button(text="Start experiment", command=self.start_experiment)
        start_experiment_button.pack()

    def build_segmentation_frame(self):
        segmentation_frame = Frame(self)
        segmentation_frame.pack(fill=X)

        segmentation_label = Label(segmentation_frame, text="Segmentation")
        segmentation_label.pack(side=LEFT, padx=5, pady=5)

        sigma_frame = Frame(segmentation_frame)
        sigma_frame.pack(fill=X)
        sigma_label = Label(sigma_frame, text="Sigma")
        sigma_label.pack(side=LEFT, padx=5, pady=5)
        sigma_in = Entry(sigma_frame)
        sigma_in.pack(fill=X, padx=5, expand=True)

        tau_frame = Frame(segmentation_frame)
        tau_frame.pack(fill=X)
        tau_label = Label(tau_frame, text="Tau")
        tau_label.pack(side=LEFT, padx=5, pady=5)
        tau_in = Entry(tau_frame)
        tau_in.pack(fill=X, padx=5, expand=True)

        position_frame = Frame(segmentation_frame)
        position_frame.pack(fill=X)
        v = IntVar()
        position_in = Checkbutton(position_frame, text="Use position", variable=v)
        position_in.var = v
        position_in.pack(side=LEFT, padx=5, pady=5)

        return segmentation_frame

    @staticmethod
    def start_experiment():
        RunExperiment().start()


class RunExperiment(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print("Started thread")
        evaluator = Evaluator()
        evaluator.run_validation()

def main():
    root = Tk()
    #root.geometry("300x300+300+300")
    app = Example()
    root.mainloop()


if __name__ == '__main__':
    main()