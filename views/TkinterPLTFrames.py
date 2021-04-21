from tkinter import Frame, Button, Scrollbar

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from models.SubjectContainers import BoxOfSubjects
from models.ConfigureMe import Constants
import tkinter as tk

from views.PLT.Simulation import MovingSubjects
from views.PLT.SimulationObervers import AreaChart


class AbstractFrame(Frame):
    def __init__(self, root, col, key, config = Constants()):
        dim_dict = {}
        dim_dict["width"], dim_dict["height"] = config.get_dimensions(col, key)
        super().__init__(root, bg = config.DEFAULT_BG, **dim_dict, **config.FRAME_PADDING)
        self.components = []
        label = tk.Label(self, text = self.__class__.__name__)
        label.grid(row = 0, column = 0)

class HeaderFrame(AbstractFrame):
    def __init__(self, root, config = Constants()):
        super().__init__(root, 0, "HEADER_DIM", config)

class SimulationFrame(AbstractFrame):
    def __init__(self, root, config = Constants()):
        super().__init__(root, 2, "SIMULATION_DIM", config)


        self.ViewBox = MovingSubjects(container=BoxOfSubjects())
        self.canvas = FigureCanvasTkAgg(self.ViewBox.fig, self)
        self.canvas.get_tk_widget().grid()
        root.master.ani = self.ViewBox.start_animation()

class GraphFrame(AbstractFrame):
    def __init__(self, root, config = Constants()):
        super().__init__(root, 1, "GRAPH_DIM", config)
        self.ViewBox = AreaChart()
        self.canvas = FigureCanvasTkAgg(self.ViewBox.fig, self)
        self.canvas.get_tk_widget().grid()

class ParametersFrame(AbstractFrame):
    def __init__(self, root, config = Constants()):
        super().__init__(root, 1, "PARAMETERS_DIM", config)
        i = 0

        canvas = tk.Canvas(self)
        scrollbar = Scrollbar(self, orient = "vertical", command=canvas.yview)

        scrollable_frame = Frame(canvas, bg = config.DEFAULT_BG)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        for k,v in config.PARAMETERS.all.items():
            _consturctor = getattr(tk, v[0])
            label = tk.Label(scrollable_frame, text = v[1])
            label.grid(row = i, column = 0)
            resolution = 1/100 if v[2][1] == 1 else 1/v[2][1]
            control_element = _consturctor(scrollable_frame,
                                           from_ = v[2][0],
                                           to = v[2][1],
                                           length = 100,
                                           resolution = resolution,
                                           orient = tk.HORIZONTAL)

            control_element.grid(row = i, column = 1)
            i += 1

        canvas.grid(row=0, column=0, sticky="nwse")
        scrollbar.grid(row=0, column=1, sticky="ns")



class ScenarioFrame(AbstractFrame):
    def __init__(self, root, config = Constants()):
        super().__init__(root, 2, "SCENARIO_DIM", config)

        self.components = []

        for v in config.SCENARIO_CONFIG.values():
            self.components.append(Button(self, **v))

        for i, c in enumerate(self.components):
            c.grid(row=1, column=i)

class ButtonsFrame(AbstractFrame):

    def __init__(self, root, config = Constants()):
        super().__init__(root, 2, "BUTTONS_DIM", config)

        self.components = []

        for v in config.BUTTONS_CONFIG.values():
            self.components.append(Button(self, **v))

        for i,c in enumerate(self.components):
            c.grid(row = 1, column  = i)

class TkinterPLTBuilder():
    def __init__(self, config = Constants(), window = None):
        self.window = tk.TK() if not window else window
        self.main_components = {}
        self.main_position = {}
        self.components = {}
        self.position = {}

    def build(self):

        self.main_components["HEADER"] = HeaderFrame(self.window)
        self.main_components["LEFT"] = Frame(self.window, bg = "white")
        self.main_components["RIGHT"] =  Frame(self.window, bg = "white")


        self.components["GRAPH"] = GraphFrame(self.main_components["LEFT"])
        self.components["PARAMETERS"] = ParametersFrame(self.main_components["LEFT"])
        self.components["SIMULATION"] = SimulationFrame(self.main_components["RIGHT"])

        self.components["GRAPH"].ViewBox.observe(self.components["SIMULATION"].ViewBox)

        self.components["BUTTONS"] = ButtonsFrame(self.main_components["RIGHT"])
        self.components["SCENARIO"] = ScenarioFrame(self.main_components["RIGHT"])


        self.main_position["HEADER"] = dict(row = 0, column = 0, columnspan = 2, sticky = "we")
        self.main_position["LEFT"] = dict(row = 0, column = 0, sticky = "we")
        self.main_position["RIGHT"] = dict(row = 0, column = 1, sticky = "we")


        self.position["GRAPH"] = dict(row = 2, column = 1)
        self.position["PARAMETERS"] = dict(row = 3, column = 1)
        self.position["SIMULATION"] = dict(row = 2, column = 2)
        self.position["BUTTONS"] = dict(row = 3, column = 2)
        self.position["SCENARIO"] = dict(row = 4, column = 2)

        for frame, kwargs in zip(self.components.values(), self.position.values()):
            frame.grid(**kwargs)

        for frame, kwargs in zip(self.main_components.values(), self.main_position.values()):
            frame.grid(**kwargs)




