from abc import ABC, abstractmethod
from tkinter import Frame, Button

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from models.SubjectContainers import BoxOfSubjects
from models.conf import Constants
import tkinter as tk

from views.SubjectsBoxes import PLTBox


class AbstractFrame(Frame):
    def __init__(self, root, col, key, config = Constants):
        dim_dict = {}
        dim_dict["width"], dim_dict["height"] = config.get_dimensions(col, key)
        super().__init__(root, **dim_dict)
        self.components = []


class HeaderFrame(AbstractFrame):
    def __init__(self, root, config = Constants):
        super().__init__(root, -1, "HEADER_DIM", config)


class SimulationFrame(AbstractFrame):
    def __init__(self, root, config = Constants):
        super().__init__(root, 1, "SIMULATION_DIM", config)

        ViewBox = PLTBox(container=BoxOfSubjects())
        self.canvas = FigureCanvasTkAgg(ViewBox.fig, self)
        self.canvas.get_tk_widget().pack()
        root.ani = ViewBox.start_animation()

class GraphFrame(AbstractFrame):
    def __init__(self, root,  config = Constants):
        super().__init__(root, 0, "GRAPH_DIM", config)

class ParametersFrame(AbstractFrame):
    def __init__(self, root, config = Constants):
        super().__init__(root, 0, "PARAMETERS_DIM", config)

class ScenarioFrame(AbstractFrame):
    def __init__(self, root, config = Constants):
        super().__init__(root, 1, "SCENARIO_DIM", config)

class ButtonsFrame(AbstractFrame):

    def __init__(self, root, config = Constants):
        super().__init__(root, 1, "BUTTONS_DIM", config)

        self.components = []

        for v in config.BUTTONS_CONFIG.values():
            self.components.append(Button(self, **v))

        for c in self.components:
            c.pack()

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

        self.position["HEADER"] = dict(side=tk.TOP, fill="x")
        self.position["GRAPH"] = dict(side=tk.LEFT)
        self.position["PARAMETERS"] = dict(side=tk.LEFT)
        self.position["SIMULATION"] = dict(side=tk.RIGHT)
        self.position["BUTTONS"] = dict(side=tk.RIGHT)
        self.position["SCENARIO"] = dict(side=tk.RIGHT)

        for frame, kwargs in zip(self.components.values(), self.position.values()):
            frame.pack(**kwargs)


