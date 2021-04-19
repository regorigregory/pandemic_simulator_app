from models.conf import Constants
class TkinterButtons():
    def __init__(self, coldstart, restart, pause, clear):
        self.funcs = {}
        self.paused = False
        self.clear = clear
        self.restart = restart
        self.pause = pause

        self.funcs[Constants().BUTTONS_CONFIG["RESET"]["text"]] = self.handle_pause

        self.funcs[Constants().BUTTONS_CONFIG["START"]["text"]] = self.handle_pause
        self.funcs[Constants().BUTTONS_CONFIG["PAUSE"]["text"]] = self.handle_pause

    def handle_pause(self, event):
        if(self.paused):
            self.restart()
            self.paused = False
        else:
            self.pause()
            self.paused = True


    def bind_functions(self, buttons_frame):
        for button in buttons_frame.components:
            button.bind('<Button>',  self.funcs[button.cget("text")])