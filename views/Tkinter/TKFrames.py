import tkinter as tk
from tkinter import Frame, Button, Scrollbar, Label, Toplevel, LEFT, RIGHT, SOLID, ALL, CENTER

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from models.ConfigureMe import MainConfiguration, Theme
from views.PLT.Simulation import ConcreteSimulation
from views.Tkinter.SimulationObservers import TKAreaChart, TKStats
from views.AbstractClasses import AbstractFrame, AbstractSimulation


class IdentifiableScale(tk.Scale):
    def __init__(self, root, my_name, **kwargs):
        super().__init__(root, kwargs)
        self.my_name_is = my_name

    def get_my_name(self) -> str:
        return self.my_name_is


class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        if MainConfiguration().TOOLTIPS_ON.get():

            self.text = text
            if self.tipwindow or not self.text:
                return
            try:
                x, y, cx, cy = self.widget.bbox("insert")
            except:
                x, y, cx, cy = self.widget.bbox(ALL)
                y -= 100

            x = x + self.widget.winfo_rootx()
            y = y + cy + self.widget.winfo_rooty() + 30
            self.tipwindow = tw = Toplevel(self.widget)
            tw.wm_overrideredirect(1)
            tw.wm_geometry("+%d+%d" % (x, y))
            label = Label(tw, text=self.text, justify=LEFT, anchor="e",
                          bg=Theme().default_text, fg=Theme().default_bg, relief=SOLID, borderwidth=1,
                          font=("Roboto", "12", "normal"), padx=3, pady=3)
            label.grid(row=0, column=0, sticky="nwse")

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


def AddToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)


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
        self.widget = self.canvas.get_tk_widget()
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
        self.widget = self.canvas
        self.axis = self.ViewBox.y_axis
        self.canvas.grid(row=1, column=0, sticky="ne", pady=10, padx=10)
        self.axis.grid(row=1, column=1, sticky="we")


class HeaderFrame(tk.Frame):
    def __init__(self, root, text):
        super().__init__(root, bg=Theme().darkest_bg)
        header = tk.Label(self, text=text.upper(), **Theme().header_text_kwargs)
        header.grid(sticky="w")


class ConstantsParametersFrame(AbstractFrame):
    def __init__(self, root, key="constants"):
        super().__init__(root)
        self.header_frame = HeaderFrame(self, "Simulation constants")
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
        self.sliders = {}
        self.labels = {}
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
            self.labels[k] = label
            self.sliders[k] = control_element
            i += 1
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="we")
        canvas.grid(row=1, column=0, sticky="nwse")
        #scrollbar.grid(row=1, column=0, sticky="ns")


class LiveParametersFrame(AbstractFrame):
    def __init__(self, root):
        super().__init__(root)
        self.header_frame = HeaderFrame(self, "Live settings")
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
        self.sliders = {}
        self.labels = {}
        i = j = 0
        for k, v in MainConfiguration().PARAMETERS_UI_SETTINGS.live.items():
            _constructor = IdentifiableScale
            label = tk.Label(scrollable_frame, text=v[1], fg=Theme().default_text, bg=Theme().default_bg, anchor="w", font=("Roboto", 12))
            self.labels[k] = label
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
            self.sliders[k]=control_element
            i += 1
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="we")
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
        self.buttons = {}
        self.checkboxes = {}
        self.buttons_container = Frame(self)

        for i, tup in enumerate(MainConfiguration().CHECKBOX_CONFIG.items()):
            k,v = tup
            constructor = getattr(tk, v[0])
            var = tk.BooleanVar(master=self, name=k, value=getattr(MainConfiguration(), k))
            cb = constructor(self, variable=var, **v[1])
            self.checkboxes[k]=cb
            self.components.append(cb)
            setattr(MainConfiguration(), k, var)
            cb.grid(row=0, column=i, sticky="we")

        for i, tup in enumerate(MainConfiguration().BUTTONS_CONFIG.items()):
            k,v = tup
            b = Button(self.buttons_container, **v)
            self.components.append(b)
            self.buttons[k]=b
            b.grid(row=0, column=i, sticky="we")

        self.buttons_container.grid(row=1, column=0, columnspan=3)

    def get_checkboxes(self):
        return self.checkboxes


class TkinterPLTBuilder:
    def __init__(self, window=None):
        self.window = tk.TK() if not window else window
        self.components = {}

        self.columns = [MasterLeftFrame(self.window),
                        MasterRightFrame(self.window)]
        self.tooltips_data_dict = MainConfiguration().get_tooltips_dict()

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
        self.add_tooltips()

    def get_component(self, key):
        if key in list(self.components.keys()):
            return self.components[key]
        else:
            raise KeyError("The provided key {} does not exist.")

    def add_tooltips(self):

        for json_l1_k, json_l1_v in self.tooltips_data_dict.items():

            current_frame = self.components[json_l1_k]

            for json_attr_path, attr_value in json_l1_v.items():
                path_components = json_attr_path.split(".")
                object_attr_ref = current_frame
                for path in path_components:
                    object_attr_ref = getattr(object_attr_ref, path)
                if isinstance(attr_value, dict):
                    for deeper_key, deeper_value in object_attr_ref.items():
                        AddToolTip(object_attr_ref[deeper_key], attr_value[deeper_key])
                else:
                    AddToolTip(object_attr_ref, attr_value)
