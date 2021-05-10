from tkinter import Menu

from views.Tkinter.SplashScreens import AboutWindow, DocumentationWindow


class MyMenu(Menu):
    def __init__(self, root, **kwargs):
        super().__init__(root, kwargs)
        help = Menu(self, tearoff=0)
        help.add_command(label="About", command=AboutWindow)
        help.add_command(label="Documentation", command=DocumentationWindow)
        self.add_cascade(label="Help", menu=help)
