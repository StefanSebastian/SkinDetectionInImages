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
        placeholder_image = PhotoImage(Image.new('RGB', (200, 200), (192, 192, 192)))

        Label(self, text="Initial image:").grid(row=0, column=0)
        self.input_image_frame = Label(self, image=placeholder_image)
        self.input_image_frame.image = placeholder_image
        self.input_image_frame.grid(row=1, column=0)

        Label(self, text="Result:").grid(row=2, column=0)
        self.output_image_frame = Label(self, image=placeholder_image)
        self.output_image_frame.image = placeholder_image
        self.output_image_frame.grid(row=3, column=0)

        self.grid()

    def set_input_image(self, path):
        load = Image.open(path)
        resized = load.resize((200, 200))
        render = PhotoImage(resized)
        self.input_image_frame.config(image=render)
        self.input_image_frame.image = render
