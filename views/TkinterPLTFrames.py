from abc import ABC, abstractmethod
from tkinter import Frame, Button

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from models.SubjectContainers import BoxOfSubjects
from models.ConfigureMe import Constants
import tkinter as tk

from views.SubjectsBoxes import PLTBox


class AbstractFrame(Frame):
    def __init__(self, root, col, key, config = Constants()):
        dim_dict = {}
        dim_dict["width"], dim_dict["height"] = config.get_dimensions(col, key)
        super().__init__(root, **dim_dict, **config.FRAME_PADDING)
        self.components = []
        label = tk.Label(self, text = self.__class__.__name__)
        label.grid(row = 0, column = 0)

class HeaderFrame(AbstractFrame):
    def __init__(self, root, config = Constants()):
        super().__init__(root, -1, "HEADER_DIM", config)

class SimulationFrame(AbstractFrame):
    def __init__(self, root, config = Constants()):
        super().__init__(root, 1, "SIMULATION_DIM", config)


        ViewBox = PLTBox(container=BoxOfSubjects())
        self.canvas = FigureCanvasTkAgg(ViewBox.fig, self)
        self.canvas.get_tk_widget().grid()
        root.ani = ViewBox.start_animation()

class GraphFrame(AbstractFrame):
    def __init__(self, root,  config = Constants()):
        super().__init__(root, 0, "GRAPH_DIM", config)

class ParametersFrame(AbstractFrame):
    def __init__(self, root, config = Constants()):
        super().__init__(root, 0, "PARAMETERS_DIM", config)

class ScenarioFrame(AbstractFrame):
    def __init__(self, root, config = Constants()):
        super().__init__(root, 1, "SCENARIO_DIM", config)

        self.components = []

        for v in config.SCENARIO_CONFIG.values():
            self.components.append(Button(self, **v))

        for i, c in enumerate(self.components):
            c.grid(row=1, column=i)

class ButtonsFrame(AbstractFrame):

    def __init__(self, root, config = Constants()):
        super().__init__(root, 1, "BUTTONS_DIM", config)

        self.components = []

        for v in config.BUTTONS_CONFIG.values():
            self.components.append(Button(self, **v))

        for i,c in enumerate(self.components):
            c.grid(row = 1, column  = i)

class TkinterPLTBuilder():
    def __init__(self, config = Constants(), window = None):
        self.window = tk.TK() if not window else window
        self.components = {}
        self.position = {}

    def build(self):
        self.components["HEADER"] = HeaderFrame(self.window)
        self.components["GRAPH"] = GraphFrame(self.window)
        self.components["PARAMETERS"] = ParametersFrame(self.window)
        self.components["SIMULATION"] = SimulationFrame(self.window)
        self.components["BUTTONS"] = ButtonsFrame(self.window)
        self.components["SCENARIO"] = ScenarioFrame(self.window)

        self.position["HEADER"] = dict(row = 1, column = 1, rowspan = 2)
        self.position["GRAPH"] = dict(row = 2, column = 1)
        self.position["PARAMETERS"] = dict(row = 3, column = 1)
        self.position["SIMULATION"] = dict(row = 2, column = 2)
        self.position["BUTTONS"] = dict(row = 3, column = 2)
        self.position["SCENARIO"] = dict(row = 4, column = 2)

        for frame, kwargs in zip(self.components.values(), self.position.values()):
            frame.grid(**kwargs)


