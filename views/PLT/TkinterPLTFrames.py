from tkinter import Frame, Button, Scrollbar

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from models.SubjectContainers import BoxOfSubjects
from models.ConfigureMe import MainConfiguration
import tkinter as tk

from views.PLT.Simulation import ConcreteSimulation
from views.PLT.SimulationObervers import AreaChart
from views.Tkinter.SimulationObservers import TKAreaChart, TKStats


class AbstractFrame(Frame):
    def __init__(self, root, col, key, config = MainConfiguration(), grid_kwargs = {}):
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
    def __init__(self, root, config = MainConfiguration()):
        super().__init__(root, 0, "HEADER_DIM", config)


class MainFrame(AbstractFrame):
    def __init__(self, root, config = MainConfiguration(), side ="MasterLeftFrame"):
        side_index = 1 if side == "MasterLeftFrame" else 2
        super().__init__(root, side_index, "HEADER_DIM", config, grid_kwargs = config.GRID_KWARGS[side])


class SimulationFrame(AbstractFrame):
    def __init__(self, root, config = MainConfiguration()):
        super().__init__(root, 2, "SIMULATION_DIM", config)


        self.ViewBox = ConcreteSimulation(container=BoxOfSubjects())
        self.canvas = FigureCanvasTkAgg(self.ViewBox.fig, self)
        self.canvas.get_tk_widget().grid()
        self.ViewBox.start_animation()

    def get_animated_object(self):
        return self.ViewBox

class GraphFrame(AbstractFrame):
    def __init__(self, root, config = MainConfiguration()):
        super().__init__(root, 2, "GRAPH_DIM", config)
        self.ViewBox = TKAreaChart(root = self)
        self.canvas = self.ViewBox.fig
        self.canvas.grid()

class IdentifiableScale(tk.Scale):
    def __init__(self, root, my_name , **kwargs):
        super().__init__(root, kwargs)
        self.my_name_is = my_name


class ParametersFrame(AbstractFrame):
    def __init__(self, root, config = MainConfiguration()):
        super().__init__(root, 1, "PARAMETERS_DIM", config)
        i = 0
        dims = config.get_dimensions(1, "PARAMETERS_DIM")

        canvas = tk.Canvas(self, width = dims[0], height = dims[1])

        scrollbar = Scrollbar(self, orient = "vertical", command=canvas.yview)

        scrollable_frame = Frame(canvas, bg = config.DEFAULT_BG, width = dims[0])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width = dims[0])

        canvas.configure(yscrollcommand=scrollbar.set)
        self.sliders = []

        for k, v in config.PARAMETERS_UI_SETTINGS.general.items():
            _constructor = IdentifiableScale
            label = tk.Label(scrollable_frame, text = v[1], bg = config.DEFAULT_BG)
            label.grid(row = i, column = 0, sticky = "we")

            resolution = 1/100 if v[2][1] == 1 else 1

            control_element = _constructor(scrollable_frame,
                                           k,
                                           from_ = v[2][0],
                                           to = v[2][1],
                                           length=dims[0]/2,
                                           resolution = resolution,
                                           orient = tk.HORIZONTAL,
                                           bg = config.DEFAULT_BG)
            if "RANGE" in k:
                config_key = k[0:-4]
                index = 0 if "MIN" not in k else 1
                config_value = getattr(MainConfiguration(), config_key)[index]
            else:
                config_value = getattr(MainConfiguration(), k)
            control_element.set(config_value)




            control_element.grid(row = i + 1, column = 0, sticky = "we")
            self.sliders.append(control_element)
            i += 2

        canvas.grid(row=0, column=0, sticky = "nwse")
        scrollbar.grid(row=0, column=1, sticky="ns")


class StatsFrame(AbstractFrame):
    def __init__(self, root, config = MainConfiguration()):
        super().__init__(root, 2, "STATS_DIM", config)

        self.ViewBox =TKStats(self)


class ScenarioFrame(AbstractFrame):
    def __init__(self, root, config = MainConfiguration()):
        super().__init__(root, 1, "SCENARIO_DIM", config)

        self.components = []

        for v in config.SCENARIO_CONFIG.values():
            self.components.append(Button(self, **v))

        for i, c in enumerate(self.components):
            c.grid(row=1, column=i)

class ButtonsFrame(AbstractFrame):

    def __init__(self, root, config = MainConfiguration()):
        super().__init__(root, 2, "BUTTONS_DIM", config)

        self.components = []

        for v in config.BUTTONS_CONFIG.values():
            self.components.append(Button(self, **v))

        for i,c in enumerate(self.components):
            c.grid(row = 1, column  = i)


class TkinterPLTBuilder():
    def __init__(self, config = MainConfiguration(), window = None):
        self.window = tk.TK() if not window else window
        self.components = {}

    def build(self):
        # master grid components
        #self.components["MasterHeaderFrame"] = MasterHeaderFrame(self.window)
        self.components["MasterLeftFrame"] = MainFrame(self.window, side = "MasterLeftFrame")
        self.components["MasterRightFrame"] = MainFrame(self.window, side = "MasterRightFrame")
        # child components
        self.components["ScenarioFrame"] = ScenarioFrame(self.components["MasterLeftFrame"])
        self.components["ParametersFrame"] = ParametersFrame(self.components["MasterLeftFrame"])
        self.components["GraphFrame"] = GraphFrame(self.components["MasterRightFrame"])
        self.components["StatsFrame"] = StatsFrame(self.components["MasterRightFrame"])
        self.components["SimulationFrame"] = SimulationFrame(self.components["MasterRightFrame"])
        self.components["ButtonsFrame"] = ButtonsFrame(self.components["MasterRightFrame"])

        # The plot observing the simulation
        self.components["GraphFrame"].ViewBox.observe(self.components["SimulationFrame"].ViewBox)
        self.components["StatsFrame"].ViewBox.observe(self.components["SimulationFrame"].ViewBox)


        for v in self.components.values():
            v.grid()

    def get_component(self, key):
        if key in list(self.components.keys()):
            return self.components[key]
        else:
            raise KeyError("The provided key {} does not exist.")




