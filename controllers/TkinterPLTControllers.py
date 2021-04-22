from models.ConfigureMe import Constants
class TkinterButtons():
    def __init__(self, animated_object):
        self.funcs = {}
        self.paused = False
        self.reset = animated_object.reset
        self.pause = animated_object.pause
        self.resume = animated_object.resume

        self.funcs[Constants().BUTTONS_CONFIG["RESET"]["text"]] = self.handle_clear

        self.funcs[Constants().BUTTONS_CONFIG["PAUSE"]["text"]] = self.handle_pause

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

    def bind_functions(self, buttons_frame):
        self.buttons = buttons_frame.components
        for button in buttons_frame.components:
            button.bind('<Button>',  self.funcs[button.cget("text")])