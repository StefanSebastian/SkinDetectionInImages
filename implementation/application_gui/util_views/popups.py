from tkinter import Toplevel, Label


class Popups:
    @staticmethod
    def show_error_popup(parent, message, errors):
        toplevel = Toplevel(parent)
        Label(toplevel, text=message).pack()
        for error in errors:
            Label(toplevel, text=error).pack()