from models.ConfigureMe import MainConfiguration, Theme

from tkinter import Tk, PhotoImage
import os

from views.Tkinter.SplashScreens import WelcomeWindow, AboutWindow
from views.Tkinter.TKFrames import TkinterPLTBuilder
from views.Tkinter.MyMenu import MyMenu
import controllers.TkinterPLTControllers as Controllers

class MainWindow(Tk):
    _instance = None

    def __init__(self, splash_screen: Tk):
        super().__init__()
        MainWindow._instance = self
        self.splash_screen = splash_screen
        self.build()

    def build(self):
        self.splash_screen.destroy()

        window = self
        window.title(MainConfiguration().APPLICATION_TITLE)
        window.configure({"bg": Theme().default_bg})
        print(os.path.isfile(os.path.join(".", "assets", "pandemic_app_icon.png")))
        icon = PhotoImage(master=window, file=os.path.join(".", "assets", "pandemic_app_icon.png"))

        window.iconphoto(True, icon)

        window.geometry(MainConfiguration().get_main_canvas_size_tkinter())

        self.view_builder = TkinterPLTBuilder(window=window)
        self.view_builder.build()

        self.buttons_controller = Controllers.TkinterButtons(
            self.view_builder.get_component("SimulationFrame").get_animated_object())

        self.sliders_controller = Controllers.TkinterSimulationSettings()

        action = '<Button>'
        element = self.view_builder.get_component("ScenarioFrame").buttons["RESET"]

        self.reset_settings_controller = Controllers.LambdaController()
        self.reset_settings_controller.bind_functions(element, action, self.reset_to_defaults)

        self.buttons_controller.bind_functions(self.view_builder.components["ScenarioFrame"].buttons)
        self.sliders_controller.bind_functions(self.view_builder.get_component("ConstantsParametersFrame").sliders)
        self.sliders_controller.bind_functions(self.view_builder.get_component("LiveParametersFrame").sliders)

        m = MyMenu(window)
        window.configure(menu=m)
        window.protocol("WM_DELETE_WINDOW", MainWindow.handle_close_event)

    def reset_to_defaults(self, event):

        scales = list(self.view_builder.get_component("ConstantsParametersFrame").sliders.values())
        scales.extend(list(self.view_builder.get_component("LiveParametersFrame").sliders.values()))

        MainConfiguration().load_defaults()
        for scale in scales:
            attr_name = scale.get_my_name()
            attr_value = getattr(MainConfiguration(), attr_name)
            scale.set(attr_value)


    @staticmethod
    def handle_close_event():
        AboutWindow.handle_close_event()
        MainWindow._instance.destroy()
        MainWindow._instance = None

if __name__ == "__main__":

    x = WelcomeWindow(MainWindow)
