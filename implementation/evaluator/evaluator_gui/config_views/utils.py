from tkinter import filedialog


def browse_file(label):
    path = filedialog.askopenfilename()
    label.config(text=get_filename_from_path(path))


def get_filename_from_path(path):
    return path.split('/')[-1]
