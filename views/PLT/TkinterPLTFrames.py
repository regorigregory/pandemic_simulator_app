from tkinter import Frame, Button, Scrollbar

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from models.SubjectContainers import BoxOfSubjects
from models.ConfigureMe import MainConfiguration
import tkinter as tk

from views.PLT.Simulation import ConcreteSimulation
from views.PLT.SimulationObervers import AreaChart
from views.Tkinter.SimulationObservers import TKAreaChart, TKStats


class AbstractFrame(Frame):
    def __init__(self, root, config = MainConfiguration()):
        self.config = config
        self.dim_dict = {"width": (self.config.get_dimensions(self.__class__.__name__))[0],
                         "height": (self.config.get_dimensions(self.__class__.__name__))[1]}
        self.frame_settings = self.config.FRAME_SETTINGS[self.__class__.__name__]
        super().__init__(root, bg = config.DEFAULT_BG, **self.dim_dict,
                         **config.FRAME_PADDING)
        self.components = []
        self.grid_kwargs = self.frame_settings["grid_kwargs"]

    def grid(self, **kwargs):
        if(len(kwargs) == 0):
            super().grid(**self.grid_kwargs)
        else:
            super().grid(kwargs)


class MasterHeaderFrame(AbstractFrame):
    def __init__(self, root):
        super().__init__(root)


class MasterLeftFrame(AbstractFrame):
    def __init__(self, root):
        super().__init__(root)

class MasterRightFrame(AbstractFrame):
    def __init__(self, root):
        super().__init__(root)


class SimulationFrame(AbstractFrame):
    def __init__(self, root):
        super().__init__(root)


        self.ViewBox = ConcreteSimulation(container=BoxOfSubjects())
        self.canvas = FigureCanvasTkAgg(self.ViewBox.fig, self)
        self.canvas.get_tk_widget().grid()
        self.ViewBox.start_animation()

    def get_animated_object(self):
        return self.ViewBox


class GraphFrame(AbstractFrame):
    def __init__(self, root):
        super().__init__(root)
        self.ViewBox = TKAreaChart(root = self)
        self.canvas = self.ViewBox.fig
        self.canvas.grid()


class IdentifiableScale(tk.Scale):
    def __init__(self, root, my_name , **kwargs):
        super().__init__(root, kwargs)
        self.my_name_is = my_name


class ParametersFrame(AbstractFrame):
    def __init__(self, root):
        super().__init__(root)

        canvas = tk.Canvas(self, **self.dim_dict)

        scrollbar = Scrollbar(self, orient = "vertical", command=canvas.yview)

        scrollable_frame = Frame(canvas, bg = self.config.DEFAULT_BG, width = self.dim_dict["width"])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width = self.dim_dict["width"])

        canvas.configure(yscrollcommand=scrollbar.set)
        self.sliders = []
        i = j = 0
        for k, v in self.config.PARAMETERS_UI_SETTINGS.general.items():
            _constructor = IdentifiableScale
            label = tk.Label(scrollable_frame, text = v[1], bg = self.config.DEFAULT_BG)
            col = j % 2
            j += 1

            label.grid(row = i, column = col, sticky = "we")
            resolution = 1/100 if v[2][1] == 1 else 1
            if "RANGE" not in k:
                min, max = v[2]
            elif "MIN" in k:
                min, max = v[2][0], v[2][0] + v[2][1] /2
            else:
                min, max = v[2][0] + v[2][1] /2, v[2][1]

            control_element = _constructor(scrollable_frame,
                                           k,
                                           from_ = min,
                                           to = max,
                                           length=self.dim_dict["width"] / 2,
                                           resolution = resolution,
                                           orient = tk.HORIZONTAL,
                                           bg = self.config.DEFAULT_BG)

            if "RANGE" in k:
                config_key = k[0:-4]
                index = 0 if "MIN" not in k else 1
                config_value = getattr(MainConfiguration(), config_key)[index]
            elif "SUBJECT_VELOCITY" == k:
                config_value = getattr(MainConfiguration(), k)[1]
            else:
                config_value = getattr(MainConfiguration(), k)
            control_element.set(config_value)

            col = j % 2
            j += 1
            control_element.grid(row = i , column = col, sticky = "we")
            self.sliders.append(control_element)
            i += 1
        canvas.grid(row=0, column=1, sticky = "nwse")
        scrollbar.grid(row=0, column=0, sticky="ns")


class StatsFrame(AbstractFrame):
    def __init__(self, root):
        super().__init__(root)
        self.ViewBox =TKStats(self)


class ScenarioFrame(AbstractFrame):
    def __init__(self, root):
        super().__init__(root)

        self.components = []
        self.checkboxes = dict()

        for v in self.config.SCENARIO_CONFIG.values():
            constructor = getattr(tk, v[0])
            self.components.append(constructor(self, **v[1]))
        for k, v in self.config.CHECKBOX_CONFIG.items():
            constructor = getattr(tk, v[0])
            var = tk.BooleanVar(master = self, name = k, value = False)
            self.checkboxes[k] = constructor(self, variable = var, **v[1])
            self.components.append(self.checkboxes[k])
            setattr(MainConfiguration(), k, var)

        for i, c in enumerate(self.components):
            c.grid(row=1, column=i)

    def get_checkboxes(self):
        return self.checkboxes


class ButtonsFrame(AbstractFrame):

    def __init__(self, root):
        super().__init__(root)

        self.components = []

        for v in self.config.BUTTONS_CONFIG.values():
            self.components.append(Button(self, **v))

        for i,c in enumerate(self.components):
            c.grid(row = 1, column  = i)


class TkinterPLTBuilder():
    def __init__(self, config = MainConfiguration(), window = None):
        self.window = tk.TK() if not window else window
        self.config = config
        self.components = {}

        self.columns = [MasterLeftFrame(self.window),
                         MasterRightFrame(self.window)]

    def build(self):
        # master grid components
        #self.components["MasterHeaderFrame"] = MasterHeaderFrame(self.window)
        frames = [ScenarioFrame, ParametersFrame, GraphFrame, StatsFrame, SimulationFrame, ButtonsFrame]
        # child components
        for f in frames:
            name = f.__name__
            frame_settings = self.config.FRAME_SETTINGS[name]
            parent = self.columns[frame_settings["column"]]
            self.components[name] = f(parent)
            self.components[name].grid(**frame_settings["grid_kwargs"])

        # The plot observing the simulation
        self.components["GraphFrame"].ViewBox.observe(self.components["SimulationFrame"].ViewBox)
        self.components["StatsFrame"].ViewBox.observe(self.components["SimulationFrame"].ViewBox)

        self.columns[0].grid(**self.config.FRAME_SETTINGS["MasterLeftFrame"]["grid_kwargs"])
        self.columns[1].grid(**self.config.FRAME_SETTINGS["MasterRightFrame"]["grid_kwargs"])

    def get_component(self, key):
        if key in list(self.components.keys()):
            return self.components[key]
        else:
            raise KeyError("The provided key {} does not exist.")




