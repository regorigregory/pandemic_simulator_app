from tkinter import Menu


class MyMenu(Menu):
    def __init__(self, root, **kwargs):
        super().__init__(root, kwargs)
        help = Menu(self, tearoff=0)
        help.add_command(label="About", command=None)
        help.add_command(label="Documentation", command=None)
        self.add_cascade(label="Help", menu=help)
