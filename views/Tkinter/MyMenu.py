from tkinter import Menu, Checkbutton, BooleanVar
from models.ConfigureMe import MainConfiguration
from views.Tkinter.SplashScreens import AboutWindow


class MyMenu(Menu):
    def __init__(self, root, **kwargs):
        super().__init__(root, kwargs)
        help = Menu(self, tearoff=0)
        help.add_command(label="About", command=AboutWindow)
        var = BooleanVar()
        var.set(MainConfiguration().TOOLTIPS_ON)
        MainConfiguration().TOOLTIPS_ON = var
        help.add_checkbutton(label="Tooltips", variable=var)
        self.add_cascade(label="Help", menu=help)
