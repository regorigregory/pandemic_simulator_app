import tkinter as tk
from tkinter import Frame, Button, Scrollbar

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from models.ConfigureMe import MainConfiguration, Theme
from views.PLT.Simulation import ConcreteSimulation
from views.Tkinter.SimulationObservers import TKAreaChart, TKStats


class AbstractFrame(Frame):
    def __init__(self, root, config=MainConfiguration()):
        self.config = config
        self.dim_dict = {"width": (self.config.get_frame_dimensions_of(self.__class__.__name__))[0],
                         "height": (self.config.get_frame_dimensions_of(self.__class__.__name__))[1]}
        self.frame_settings = self.config.FRAME_SETTINGS[self.__class__.__name__]
        super().__init__(root, bg=config.DEFAULT_BG, **self.dim_dict,
                         **config.FRAME_PADDING)
        self.components = []
        self.grid_kwargs = self.frame_settings["grid_kwargs"]

    def grid(self, **kwargs):
        if len(kwargs) == 0:
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

        self.ViewBox = ConcreteSimulation()
        self.ViewBox.fig.subplots_adjust(left=0, bottom=0.1, right=0.95, top=1, wspace=0, hspace=0)
        self.canvas = FigureCanvasTkAgg(self.ViewBox.fig, self)

        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="n", ipady=0, pady=0)
        self.ViewBox.start_animation()

    def get_animated_object(self):
        return self.ViewBox


class GraphFrame(AbstractFrame):
    def __init__(self, root):
        super().__init__(root)
        self.ViewBox = TKAreaChart(root=self)
        self.canvas = self.ViewBox.fig
        self.canvas.grid(row=1, column=0, sticky="w")


class IdentifiableScale(tk.Scale):
    def __init__(self, root, my_name, **kwargs):
        super().__init__(root, kwargs)
        self.my_name_is = my_name


class ParametersFrame(AbstractFrame):
    def __init__(self, root):
        super().__init__(root)

        header = tk.Label(self, text="Simulation settings", bg=Theme().default_bg, font=("Courier", 14))
        canvas = tk.Canvas(self, **self.dim_dict, bg=Theme().default_bg)

        scrollbar = Scrollbar(self, orient="vertical", command=canvas.yview)

        scrollable_frame = Frame(canvas, bg=self.config.DEFAULT_BG, width=self.dim_dict["width"])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=self.dim_dict["width"])

        canvas.configure(yscrollcommand=scrollbar.set)
        self.sliders = []
        i = j = 0
        for k, v in self.config.PARAMETERS_UI_SETTINGS.general.items():
            _constructor = IdentifiableScale
            label = tk.Label(scrollable_frame, text=v[1], bg=self.config.DEFAULT_BG)
            col = j % 2
            j += 1

            label.grid(row=i, column=col, sticky="we")
            resolution = 1 / 100 if v[2][1] == 1 else 1
            min_, max_ = v[2]


            control_element = _constructor(scrollable_frame,
                                           k,
                                           from_=min_,
                                           to=max_,
                                           length=self.dim_dict["width"] / 2,
                                           resolution=resolution,
                                           orient=tk.HORIZONTAL,
                                           bg=self.config.DEFAULT_BG)

            if "SUBJECT_VELOCITY" == k:
                config_value = getattr(MainConfiguration(), k)[1]
            else:
                config_value = getattr(MainConfiguration(), k)
            control_element.set(config_value)

            col = j % 2
            j += 1
            control_element.grid(row=i, column=col, sticky="we")
            self.sliders.append(control_element)
            i += 1
        header.grid(row=0, column=0, columnspan=2)
        canvas.grid(row=1, column=1, sticky="nwse")
        scrollbar.grid(row=1, column=0, sticky="ns")


class StatsFrame(AbstractFrame):
    def __init__(self, root):
        super().__init__(root)
        self.header = tk.Label(self, text="Simulation statistics", font=("Courier", 14), bg=Theme().default_bg)
        self.header.grid(row=0, column=0, columnspan=3)

        self.ViewBox = TKStats(self)


class ScenarioFrame(AbstractFrame):
    def __init__(self, root):
        super().__init__(root)

        self.components = []
        self.buttons = []
        self.checkboxes = []

        for k, v in self.config.CHECKBOX_CONFIG.items():
            constructor = getattr(tk, v[0])
            var = tk.BooleanVar(master=self, name=k, value=getattr(self.config, k))
            cb = constructor(self, variable=var, **v[1])
            self.checkboxes.append(cb)
            self.components.append(cb)
            setattr(MainConfiguration(), k, var)

        for i, v in enumerate(self.checkboxes):
            v.grid(row=0, column=i, sticky="we")

        self.buttons_container = Frame(self)

        for v in self.config.BUTTONS_CONFIG.values():
            b = Button(self.buttons_container, **v)
            self.components.append(b)
            self.buttons.append(b)
        self.buttons[0].grid(row=0, column=0, sticky="we")
        self.buttons[1].grid(row=0, column=1, sticky="we")
        self.buttons_container.grid(row=1, column=0, columnspan=3)

    def get_checkboxes(self):
        return self.checkboxes


class ButtonsFrame(AbstractFrame):

    def __init__(self, root):
        super().__init__(root)

        self.components = []

        for v in self.config.BUTTONS_CONFIG.values():
            self.components.append(Button(self, **v))

        for i, c in enumerate(self.components):
            c.grid(row=1, column=i)


class TkinterPLTBuilder:
    def __init__(self, config=MainConfiguration(), window=None):
        self.window = tk.TK() if not window else window
        self.config = config
        self.components = {}

        self.columns = [MasterLeftFrame(self.window),
                        MasterRightFrame(self.window)]

    def build(self):
        # master grid components
        # self.components["MasterHeaderFrame"] = MasterHeaderFrame(self.window)
        frames = [ScenarioFrame, ParametersFrame, GraphFrame, StatsFrame, SimulationFrame]
        # ButtonsFrame has been removed
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
