from models.ConfigureMe import MainConfiguration
from abc import ABC, abstractmethod


class AbstractController(ABC):
    def __init__(self):
        self.ui_elements = []
    @abstractmethod
    def bind_functions(self, frame_of_elements):
        pass


class TkinterButtons(AbstractController):
    def __init__(self, animated_object):
        self.funcs = {}
        self.paused = False
        self.reset = animated_object.reset
        self.pause = animated_object.pause
        self.resume = animated_object.resume

        self.funcs[MainConfiguration().BUTTONS_CONFIG["RESET"]["text"]] = self.handle_clear

        self.funcs[MainConfiguration().BUTTONS_CONFIG["PAUSE"]["text"]] = self.handle_pause

    def handle_pause(self, event):
        if(self.paused):
            self.resume()
            self.paused = False
            event.widget.configure(text = "Pause")
        else:
            self.pause()
            self.paused = True
            event.widget.configure(text = "Continue")


    def handle_clear(self, event):
        self.reset()

    def bind_functions(self, buttons):
        self.ui_elements = buttons
        for button in self.ui_elements:
            button.bind('<Button>',  self.funcs[button.cget("text")])

class TkinterSimulationSettings(AbstractController):
    def __init__(self):
        super().__init__()

    def update_config(self, event):
        key = event.widget.my_name_is
        value = event.widget.get()
        setattr(MainConfiguration(), key, value)


    def bind_functions(self, sliders):
        self.ui_elements = sliders
        for slider in self.ui_elements:
            slider.bind("<ButtonRelease>", self.update_config)

class LambdaController(AbstractController):
    def bind_functions(self, element, action, function):
        self.ui_elements.append(element)
        element.bind(action, function)
