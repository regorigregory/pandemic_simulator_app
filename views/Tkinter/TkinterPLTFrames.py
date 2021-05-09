import tkinter as tk
from tkinter import Frame, Button, Scrollbar

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from models.ConfigureMe import MainConfiguration, Theme
from views.PLT.Simulation import ConcreteSimulation
from views.Tkinter.SimulationObservers import TKAreaChart, TKStats
from views.AbstractClasses import AbstractFrame, AbstractSimulation


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
        self.canvas = FigureCanvasTkAgg(self.ViewBox.fig, self)
        self.canvas.get_tk_widget().configure(bg=Theme().default_bg, highlightthickness=0, bd=0, relief='ridge')
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="n", ipady=0, pady=0)
        #self.ViewBox.start_animation()

    def get_animated_object(self) -> AbstractSimulation:
        return self.ViewBox


class GraphFrame(AbstractFrame):
    def __init__(self, root):
        super().__init__(root)
        self.ViewBox = TKAreaChart(root=self)
        self.canvas = self.ViewBox.fig
        self.axis = self.ViewBox.y_axis
        self.canvas.grid(row=1, column=0, sticky="ne", pady=10, padx=10)
        self.axis.grid(row=1, column=1, sticky="we")


class IdentifiableScale(tk.Scale):
    def __init__(self, root, my_name, **kwargs):
        super().__init__(root, kwargs)
        self.my_name_is = my_name

    def get_my_name(self)->str:
        return self.my_name_is


class HeaderFrame(tk.Frame):
    def __init__(self, root, text):
        super().__init__(root, bg=Theme().darkest_bg)
        header = tk.Label(self, text=text.upper(), **Theme().header_text_kwargs)
        header.grid(sticky="w")


class ConstantsParametersFrame(AbstractFrame):
    def __init__(self, root, key="constants"):
        super().__init__(root)
        header_frame = HeaderFrame(self, "Simulation constants")
        canvas = tk.Canvas(self, **self.dim_dict, bg=Theme().default_bg, highlightthickness=0, bd=0, relief='ridge')

        #scrollbar = Scrollbar(self, orient="vertical", command=canvas.yview)

        scrollable_frame = Frame(canvas, bg=Theme().default_bg, width=self.dim_dict["width"], pady= 20, highlightthickness=0, bd=0)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=self.dim_dict["width"])

        #canvas.configure(yscrollcommand=scrollbar.set)
        self.sliders = []
        i = j = 0
        for k, v in MainConfiguration().PARAMETERS_UI_SETTINGS.constants.items():
            _constructor = IdentifiableScale
            label = tk.Label(scrollable_frame, text=v[1], fg=Theme().default_text, bg=Theme().default_bg, anchor="w", font=("Roboto", 12))
            col = j % 2
            j += 1

            label.grid(row=i, column=col, sticky="e")
            resolution = 1 / 100 if v[2][1] == 1 else 1
            min_, max_ = v[2]

            control_element = _constructor(scrollable_frame,
                                           k,
                                           from_=min_,
                                           to=max_,
                                           length=self.dim_dict["width"] / 2 + 10,
                                           resolution=resolution,
                                           orient=tk.HORIZONTAL,
                                           fg=Theme().default_text,
                                           bg=Theme().default_bg,
                                           highlightthickness=0,
                                           bd=3)

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
        header_frame.grid(row=0, column=0, columnspan=2, sticky="we")
        canvas.grid(row=1, column=0, sticky="nwse")
        #scrollbar.grid(row=1, column=0, sticky="ns")


class LiveParametersFrame(AbstractFrame):
    def __init__(self, root):
        super().__init__(root)
        header_frame = HeaderFrame(self, "Live settings")
        canvas = tk.Canvas(self, **self.dim_dict, bg=Theme().default_bg, highlightthickness=0, bd=0, relief='ridge')

        #scrollbar = Scrollbar(self, orient="vertical", command=canvas.yview)

        scrollable_frame = Frame(canvas, bg=Theme().default_bg, width=self.dim_dict["width"], pady= 20, highlightthickness=0, bd=0)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=self.dim_dict["width"])

        #canvas.configure(yscrollcommand=scrollbar.set)
        self.sliders = []
        i = j = 0
        for k, v in MainConfiguration().PARAMETERS_UI_SETTINGS.live.items():
            _constructor = IdentifiableScale
            label = tk.Label(scrollable_frame, text=v[1], fg=Theme().default_text, bg=Theme().default_bg, anchor="w", font=("Roboto", 12))
            col = j % 2
            j += 1

            label.grid(row=i, column=col, sticky="e")
            resolution = 1 / 100 if v[2][1] == 1 else 1
            min_, max_ = v[2]


            control_element = _constructor(scrollable_frame,
                                           k,
                                           from_=min_,
                                           to=max_,
                                           length=self.dim_dict["width"] / 2 + 10,
                                           resolution=resolution,
                                           orient=tk.HORIZONTAL,
                                           fg=Theme().default_text,
                                           bg=Theme().default_bg,
                                           highlightthickness=0,
                                           bd=3)

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
        header_frame.grid(row=0, column=0, columnspan=2, sticky="we")
        canvas.grid(row=1, column=0, sticky="nwse")


class StatsFrame(AbstractFrame):
    def __init__(self, root):
        super().__init__(root)
        self.header_frame = HeaderFrame(self, "Simulation statistics")
        self.header_frame.grid(row=0, column=0, columnspan=3, sticky="we")

        self.ViewBox = TKStats(self)


class ScenarioFrame(AbstractFrame):
    def __init__(self, root):
        super().__init__(root)

        self.components = []
        self.buttons = []
        self.checkboxes = []

        for k, v in MainConfiguration().CHECKBOX_CONFIG.items():
            constructor = getattr(tk, v[0])
            var = tk.BooleanVar(master=self, name=k, value=getattr(MainConfiguration(), k))
            cb = constructor(self, variable=var, **v[1])
            self.checkboxes.append(cb)
            self.components.append(cb)
            setattr(MainConfiguration(), k, var)

        for i, v in enumerate(self.checkboxes):
            v.grid(row=0, column=i, sticky="we")

        self.buttons_container = Frame(self)

        for i, v in enumerate(MainConfiguration().BUTTONS_CONFIG.values()):
            b = Button(self.buttons_container, **v)
            self.components.append(b)
            self.buttons.append(b)
            b.grid(row=0, column=i, sticky="we")

        self.buttons_container.grid(row=1, column=0, columnspan=3)

    def get_checkboxes(self):
        return self.checkboxes


class ButtonsFrame(AbstractFrame):

    def __init__(self, root):
        super().__init__(root)

        self.components = []

        for v in MainConfiguration().BUTTONS_CONFIG.values():
            self.components.append(Button(self, **v))

        for i, c in enumerate(self.components):
            c.grid(row=1, column=i)


class TkinterPLTBuilder:
    def __init__(self, window=None):
        self.window = tk.TK() if not window else window
        self.components = {}

        self.columns = [MasterLeftFrame(self.window),
                        MasterRightFrame(self.window)]

    def build(self):
        # master grid components
        # self.components["MasterHeaderFrame"] = MasterHeaderFrame(self.window)
        frames = [ScenarioFrame, ConstantsParametersFrame, LiveParametersFrame, GraphFrame, StatsFrame, SimulationFrame]
        # ButtonsFrame has been removed
        # child components
        for f in frames:
            name = f.__name__
            frame_settings = MainConfiguration().GRID_SETTINGS[name]
            parent = self.columns[frame_settings["column"]]
            self.components[name] = f(parent)
            self.components[name].grid()

        # The plot observing the simulation
        self.components["GraphFrame"].ViewBox.observe(self.components["SimulationFrame"].ViewBox)
        self.components["StatsFrame"].ViewBox.observe(self.components["SimulationFrame"].ViewBox)
        self.columns[0].grid(**MainConfiguration().GRID_SETTINGS["MasterLeftFrame"]["grid_kwargs"])
        self.columns[1].grid(**MainConfiguration().GRID_SETTINGS["MasterRightFrame"]["grid_kwargs"])

    def get_component(self, key):
        if key in list(self.components.keys()):
            return self.components[key]
        else:
            raise KeyError("The provided key {} does not exist.")
