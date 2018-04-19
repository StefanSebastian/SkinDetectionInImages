from tkinter import filedialog


def browse_file(label):
    filename = filedialog.askopenfilename()
    label.config(text=filename)
