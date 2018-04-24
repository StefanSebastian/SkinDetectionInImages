from tkinter.ttk import Frame, Label

import cv2
from PIL import Image
from PIL.ImageTk import PhotoImage


class ImageDisplayFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.input_image_frame = None
        self.output_image_frame = None

        self.init_ui()

    def init_ui(self):
        self.input_image_frame = Label(self)
        self.input_image_frame.grid(row=0, column=0)

        self.output_image_frame = Label(self)
        self.output_image_frame.grid(row=1, column=0)

        self.grid()

    def set_input_image(self, path):
        load = Image.open(path)
        resized = load.resize((200, 200))
        render = PhotoImage(resized)
        self.input_image_frame.config(image=render)
        self.input_image_frame.image = render
