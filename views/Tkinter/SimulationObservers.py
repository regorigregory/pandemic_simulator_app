
import numpy as np
import tkinter as tk
from models.ConfigureMe import Theme, MainConfiguration
from abc import ABC, abstractmethod

class Observer(ABC):
    def __init__(self):
        self.config = MainConfiguration()
        self.theme = Theme()

    @abstractmethod
    def update(self, new_data):
        pass
    def observe(self, observable):
        observable.attach(self)

    def update_logs(self, newdata):
        for k, v in newdata.items():
            if (k == "IMMUNE"):
                self.log[k] = np.concatenate(
                    (self.log[k], [[self.frames, len(v)]]), axis=0)

            else:
                self.log[k] = np.concatenate((self.log[k], [[self.frames, len(v)]]), axis=0)

class TKStats(Observer):
    def __init__(self, root):
        super().__init__()
        self.log = dict(INFECTED = [[0, 0]], SUSCEPTIBLE = [[0, 0]], IMMUNE = [[0, 0]])
        self.fig = tk.Frame(root, bg = self.theme.default_bg)
        self.ui_elements = dict()
        self.ui_elements["Infected"] = tk.Label(self.fig, text = "Infected: 0", bg = self.theme.default_bg)
        self.ui_elements["Susceptible"] = tk.Label(self.fig, text = "Susceptible: 0", bg = self.theme.default_bg)
        self.ui_elements["Immune"] = tk.Label(self.fig, text = "Immune: 0", bg = self.theme.default_bg)

        for v in self.ui_elements.values():
            v.grid()

        self.fig.grid()

    def update_stats(self, data):
        for k,v in self.ui_elements.items():
            v.configure({"text": "{}: {}".format(k, len(data[k.upper()]))})

    def update(self, data):
        self.update_stats(data)


class TKAreaChart(Observer):
    def __init__(self, root=None):
        super().__init__()
        self.width, self.height = self.config.get_dimensions(1, "GRAPH_DIM")
        self.DPI = self.config.DPI
        self.frames = 0
        self.log = dict(INFECTED = [[0, 0]], SUSCEPTIBLE = [[0, 0]], IMMUNE = [[0, 0]])

        self.fig = tk.Canvas(root, width=self.width, height = self.height, bg = self.theme.area_plot_bg)

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, x):
        self._width = x

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, y):
        self._height = y

    def update(self, new_data):
        if not new_data:
            self.frames = 0
            self.log = dict(INFECTED=[[0, 0]], SUSCEPTIBLE=[[0, 0]], IMMUNE=[[0, 0]])
            self.fig.delete("all")
        else:
            self.frames += 1
            self.update_logs(new_data)
            self.fig.delete("all")
            self.redraw_verts()

    def redraw_verts(self):
        width_frame_ratio = self._width / self.frames
        height_frame_ratio = self._height / MainConfiguration().SUBJECT_NUMBER

        infected_points = np.array(self.log["INFECTED"])


        infected_points[:, 1] =  self._height - infected_points[:, 1] * height_frame_ratio

        infected_points = np.concatenate([infected_points, [[self.frames, self._height-1]]])
        infected_points[:, 0] = infected_points[:, 0] * width_frame_ratio

        infected_points = infected_points.tolist()

        immune_points = np.concatenate([self.log["IMMUNE"], [[self.frames, 0]]])
        immune_points[:, 0] = immune_points[:, 0] * width_frame_ratio
        immune_points[:, 1] = immune_points[:, 1] * height_frame_ratio

        immune_points = immune_points.tolist()

        self.fig.create_polygon(infected_points, fill = self.theme.area_plot_colours[0])
        self.fig.create_polygon(immune_points, fill = self.theme.area_plot_colours[1])

    def observe(self, observable):
        observable.attach(self)