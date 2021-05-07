from models.ConfigureMe import MainConfiguration, Theme
from tkinter import Tk, PhotoImage
import os

from views.Tkinter.SplashScreens import WelcomeScreen
from views.TkinterPLTFrames import TkinterPLTBuilder
from views.Tkinter.MyMenu import MyMenu
import controllers.TkinterPLTControllers as Controllers


if __name__ == "__main__":

    def f(splash_screen: Tk):
        splash_screen.destroy()

        window = Tk()
        window.title("Pandemic Simulator")
        window.configure({"bg": Theme().default_bg})
        print(os.path.isfile(os.path.join(".", "assets", "pandemic_app_icon.png")))
        icon = PhotoImage(master=window, file=os.path.join(".", "assets", "pandemic_app_icon.png"))

        window.iconphoto(True, icon)

        window.geometry(MainConfiguration().get_main_canvas_size_tkinter())
        view_builder = TkinterPLTBuilder(window=window)
        view_builder.build()

        ButtonsController = Controllers.TkinterButtons(
            view_builder.get_component("SimulationFrame").get_animated_object())
        SlidersController = Controllers.TkinterSimulationSettings()

        ButtonsController.bind_functions(view_builder.components["ScenarioFrame"].buttons)
        SlidersController.bind_functions(view_builder.get_component("ConstantsParametersFrame").sliders)
        SlidersController.bind_functions(view_builder.get_component("LiveParametersFrame").sliders)

        m = MyMenu(window)
        window.configure(menu=m)


    x = WelcomeScreen(f)
