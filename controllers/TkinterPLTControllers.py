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
        self.stop = animated_object.reset
        self.pause = animated_object.pause
        self.resume = animated_object.resume
        self.start = animated_object.start
        self.funcs["Start"] = self.handle_start

        self.funcs[MainConfiguration().BUTTONS_CONFIG["START"]["text"]] = self.handle_start

        self.funcs[MainConfiguration().BUTTONS_CONFIG["STOP"]["text"]] = self.handle_clear
        self.running = False

    def handle_start(self, event):
        if not self.running:
            self.stop()
            self.ui_elements[0].configure(text="Pause")
            self.running = True
            self.start()
        elif self.paused:
            self.resume()
            self.paused = False
            event.widget.configure(text = "Pause")
        else:
            self.pause()
            self.paused = True
            event.widget.configure(text = "Continue")


    def handle_clear(self, event):
        self.stop()
        self.paused = False
        self.running = False
        self.ui_elements[0].configure(text="Start")

    def bind_functions(self, buttons):
        self.ui_elements = list(buttons.values())
        for button in self.ui_elements:
            func_key = button.cget("text")
            if func_key in self.funcs.keys():
                button.bind('<Button>',  self.funcs[button.cget("text")])


class TkinterSimulationSettings(AbstractController):
    def __init__(self):
        super().__init__()

    def update_config(self, event):
        key = event.widget.my_name_is
        value = event.widget.get()
        setattr(MainConfiguration(), key, value)

    def bind_functions(self, sliders):
        self.ui_elements = list(sliders.values())
        for slider in self.ui_elements:
            slider.bind("<ButtonRelease>", self.update_config)


class DocumentationController:
    def __init__(self):
        pass

class LambdaController(AbstractController):
    def bind_functions(self, element, action, function):
        self.ui_elements.append(element)
        element.bind(action, function)
