from tkinter import Tk, Label, mainloop, Frame, Button, ALL
import os
from PIL import ImageTk, Image
from models.ConfigureMe import MainConfiguration, Theme
from depreciated.UserGuide import ContentsBuilder


class AbstractSplashScreen(Tk):
    def __init__(self, title_prefix=""):
        super().__init__()
        self.title(title_prefix + MainConfiguration().APPLICATION_TITLE)
        icon = ImageTk.PhotoImage(master=self, file=os.path.join(".", "assets", "pandemic_app_icon.png"))
        self.iconphoto(True, icon)


class WelcomeWindow(AbstractSplashScreen):

    def __init__(self, after_function):
        super().__init__()
        MainConfiguration().MAIN_CANVAS_SIZE = [self.winfo_screenwidth(), self.winfo_screenheight()]
        self.geometry(MainConfiguration().get_main_canvas_size_tkinter())
        self.wm_overrideredirect(1)

        bg_image = ImageTk.PhotoImage(Image.open(os.path.join(".", "assets", "virus_closeup.jpg")))

        bg_container = Label(self, image=bg_image)
        app_title = Label(self, text="Pandemic simulator", font=("Roboto", 44), bg="white")
        app_subtitle = Label(self, text="version "+MainConfiguration().VERSION, font=("Roboto", 16), bg="white")
        bg_container.place(x=0, y=0, relwidth=2, relheight=2)
        app_title.place(relx=0.08, rely=0.15)
        app_subtitle.place(relx=0.08, rely=0.23)

        self.after(3000, after_function, self)
        mainloop()


class AboutWindow(AbstractSplashScreen):
    instance = None

    def __init__(self):
        if AboutWindow.instance is None:
            super().__init__(title_prefix="About - ")
            w, h = self.winfo_screenwidth(), self.winfo_screenheight()
            w0 = int(w/2-150)
            h0 = int(h/2 - 50)
            self.geometry("300x100+{}+{}".format(w0, h0))
            data = ["Pandemic simulator",
                    "Version: " + MainConfiguration().VERSION,
                    "Contact: contact.gergo.endresz@gmail.com",
                    "Released under: GNU GPL"]
            for d in data:
                Label(self, text = d).pack()
            self.protocol("WM_DELETE_WINDOW", self.handle_close_event)
            AboutWindow.instance = self

    @staticmethod
    def handle_close_event():
        if AboutWindow.instance is not None:
            AboutWindow.instance.destroy()
            AboutWindow.instance = None
