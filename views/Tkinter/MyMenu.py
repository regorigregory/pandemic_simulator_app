from tkinter import Menu


class MyMenu(Menu):
    def __init__(self, root, **kwargs):
        super().__init__(root, kwargs)
        self.add_command(label="Scenario", command=None)
        self.add_command(label="Reset to default settings", command=None)

        self.add_command(label="About", command=None)
