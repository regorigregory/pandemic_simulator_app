from tkinter import Tk, PhotoImage, Label, mainloop
import os
from PIL import ImageTk, Image
from models.ConfigureMe import MainConfiguration, Theme


class WelcomeFrame(Tk):

    def __init__(self, after_function):
        super().__init__()
        MainConfiguration().MAIN_CANVAS_SIZE = [self.winfo_screenwidth(), self.winfo_screenheight()]
        self.geometry(MainConfiguration().get_main_canvas_size_tkinter())
        self.title(MainConfiguration().APPLICATION_TITLE)

        icon = ImageTk.PhotoImage(master=self, file=os.path.join(".", "assets", "pandemic_app_icon.png"))
        logo = Image.open(os.path.join(".", "assets", "pandemic_app_icon.png"))
        logo = logo.resize([int(logo.size[0]/4), int(logo.size[1]/4)])
        logo = ImageTk.PhotoImage(logo)
        bg_image = ImageTk.PhotoImage(Image.open(os.path.join(".", "assets", "virus_closeup.jpg")))

        self.iconphoto(True, icon)

        logo_container = Label(self, image=logo, bg="white")
        #self.wm_attributes("-transparentcolor", "pink")
        bg_container = Label(self, image=bg_image)
        app_title = Label(self, text="Pandemic simulator", font=("Roboto", 44), bg="white")
        app_subtitle = Label(self, text="version 0.0.1", font=("Roboto", 16), bg="white")
        bg_container.place(x=0, y=0, relwidth=2, relheight=2)
        app_title.place(relx=0.08, rely=0.15)
        app_subtitle.place(relx=0.08, rely=0.23)

        self.after(3000, after_function, self)
        mainloop()


class AboutFrame(Tk):
    def __init__(self):
        super().__init__()


class DocumentationFrame(Tk):
    def __init__(self):
        super().__init__()
