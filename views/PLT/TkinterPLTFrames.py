from tkinter import Frame, Button, Scrollbar

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from models.SubjectContainers import BoxOfSubjects
from models.ConfigureMe import Constants
import tkinter as tk

from views.PLT.Simulation import ConcreteSimulation
from views.PLT.SimulationObervers import AreaChart


class AbstractFrame(Frame):
    def __init__(self, root, col, key, config = Constants(), grid_kwargs = {}):
        dim_dict = {}
        dim_dict["width"], dim_dict["height"] = config.get_dimensions(col, key)
        super().__init__(root, bg = config.DEFAULT_BG, **dim_dict, **config.FRAME_PADDING)
        self.components = []
        #label = tk.Label(self, text = self.__class__.__name__)
        #label.grid(row = 0, column = 0)
        self.grid_kwargs = grid_kwargs if(len(grid_kwargs)>0) else config.GRID_KWARGS[self.__class__.__name__]

    def grid(self, **kwargs):
        if(len(kwargs) == 0):
            super().grid(**self.grid_kwargs)
        else:
            super().grid(kwargs)


class MasterHeaderFrame(AbstractFrame):
    def __init__(self, root, config = Constants()):
        super().__init__(root, 0, "HEADER_DIM", config)


class MainFrame(AbstractFrame):
    def __init__(self, root, config = Constants(), side = "MasterLeftFrame"):
        super().__init__(root, 0, "HEADER_DIM", config, grid_kwargs = config.GRID_KWARGS[side])


class SimulationFrame(AbstractFrame):
    def __init__(self, root, config = Constants()):
        super().__init__(root, 2, "SIMULATION_DIM", config)


        self.ViewBox = ConcreteSimulation(container=BoxOfSubjects())
        self.canvas = FigureCanvasTkAgg(self.ViewBox.fig, self)
        self.canvas.get_tk_widget().grid()
        self.ViewBox.start_animation()

    def get_animated_object(self):
        return self.ViewBox

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
        width = config.get_dimensions(2, "PARAMETERS_DIM")[0]

        canvas = tk.Canvas(self, width = width)
        scrollbar = Scrollbar(self, orient = "vertical", command=canvas.yview)

        scrollable_frame = Frame(canvas, bg = config.DEFAULT_BG, width = width)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width = width)

        canvas.configure(yscrollcommand=scrollbar.set)

        for k,v in config.PARAMETERS.all.items():
            _consturctor = getattr(tk, v[0])
            label = tk.Label(scrollable_frame, text = v[1], bg = config.DEFAULT_BG)
            label.grid(row = i, column = 0, sticky = "we")
            resolution = 1/100 if v[2][1] == 1 else 1/v[2][1]
            control_element = _consturctor(scrollable_frame,
                                           from_ = v[2][0],
                                           to = v[2][1],
                                           length=width/2,

                                           resolution = resolution,
                                           orient = tk.HORIZONTAL,
                                           bg = config.DEFAULT_BG)

            control_element.grid(row = i, column = 1, sticky = "we")
            i += 1

        canvas.grid(row=0, column=0, sticky="nwse")
        scrollbar.grid(row=0, column=1, sticky="ns")


class StatsFrame(AbstractFrame):
    def __init__(self, root, config = Constants()):
        super().__init__(root, 2, "STATS_DIM", config)

        self.components = []

        for v in config.SCENARIO_CONFIG.values():
            self.components.append(Button(self, **v))

        for i, c in enumerate(self.components):
            c.grid(row=1, column=i)


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
        super().__init__(root, 2, "BUTTONS_DIM", config)

        self.components = []

        for v in config.BUTTONS_CONFIG.values():
            self.components.append(Button(self, **v))

        for i,c in enumerate(self.components):
            c.grid(row = 1, column  = i)


class TkinterPLTBuilder():
    def __init__(self, config = Constants(), window = None):
        self.window = tk.TK() if not window else window
        self.components = {}

    def build(self):
        # master grid components
        self.components["MasterHeaderFrame"] = MasterHeaderFrame(self.window)
        self.components["MasterLeftFrame"] = MainFrame(self.window, side = "MasterLeftFrame")
        self.components["MasterRightFrame"] = MainFrame(self.window, side = "MasterRightFrame")
        # child components
        self.components["GraphFrame"] = GraphFrame(self.components["MasterLeftFrame"])
        self.components["ScenarioFrame"] = ScenarioFrame(self.components["MasterLeftFrame"])
        self.components["ParametersFrame"] = ParametersFrame(self.components["MasterLeftFrame"])
        self.components["StatsFrame"] = StatsFrame(self.components["MasterRightFrame"])
        self.components["SimulationFrame"] = SimulationFrame(self.components["MasterRightFrame"])
        self.components["ButtonsFrame"] = ButtonsFrame(self.components["MasterRightFrame"])

        # The plot observing the simulation
        self.components["GraphFrame"].ViewBox.observe(self.components["SimulationFrame"].ViewBox)


        for v in self.components.values():
            v.grid()

    def get_component(self, key):
        if key in list(self.components.keys()):
            return self.components[key]
        else:
            raise KeyError("The provided key {} does not exist.")




