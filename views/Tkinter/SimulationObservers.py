
import numpy as np
import tkinter as tk
from models.ConfigureMe import Theme, MainConfiguration
from abc import ABC, abstractmethod

class Observer(ABC):
    def __init__(self):
        self.config = MainConfiguration()
        self.theme = Theme()
        self.subject_number = MainConfiguration().SUBJECT_NUMBER
        self.log = dict()

    @abstractmethod
    def update(self, new_data):
        pass

    def observe(self, observable):
        observable.attach(self)

    def init_log(self):
        self.log = dict(INFECTED = [[0, 0]], SUSCEPTIBLE = [[0, 0]], IMMUNE = [[0, 0]], ASYMPTOMATIC = [[0, 0]])

    def update_logs(self, newdata):
        for k, v in newdata.items():
                self.log[k] = np.concatenate((self.log[k], [[self.frames, len(v)]]), axis=0)

class TKStats(Observer):
    def __init__(self, root):
        super().__init__()
        self.init_log()
        self.fig = tk.Frame(root, bg = self.theme.default_bg)
        self.ui_elements = dict()
        self.ui_elements["Asymptomatic"] = tk.Label(self.fig, text = "Asymptomatic: 0", bg = self.theme.default_bg)
        self.ui_elements["Infected"] = tk.Label(self.fig, text = "Infected: 0", bg = self.theme.default_bg)
        self.ui_elements["Susceptible"] = tk.Label(self.fig, text = "Susceptible: 0", bg = self.theme.default_bg)
        self.ui_elements["Immune"] = tk.Label(self.fig, text = "Immune: 0", bg = self.theme.default_bg)

        for i, v in enumerate(self.ui_elements.values()):
            v.grid(row = 0, column = i)

        self.fig.grid()

    def update_stats(self, data):
        for k,v in self.ui_elements.items():
            if data:
                self.subject_number = MainConfiguration().SUBJECT_NUMBER
                v.configure({"text": "{}: {}".format(k, len(data[k.upper()]))})
            else:
                self.subject_number = self.subject_number
                v.configure({"text": "{}: {}".format(k, 0)})


    def update(self, data):
        self.update_stats(data)


class TKAreaChart(Observer):
    def __init__(self, root=None):
        super().__init__()
        self.width, self.height = self.config.get_dimensions("GraphFrame")
        self.width = self.width
        self.DPI = self.config.DPI
        self.frames = 0
        self.init_log()

        self.fig = tk.Canvas(root, width=self.width, height = self.height, bg = self.theme.plot_bg)

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
            self.subject_number = MainConfiguration().SUBJECT_NUMBER
            self.frames = 0
            self.init_log()
            self.fig.delete("all")
        else:
            self.frames += 1
            self.update_logs(new_data)
            self.fig.delete("all")
            self.redraw_verts()

    def get_area_chart_strip(self, key):
        width_frame_ratio = self._width / self.frames
        height_frame_ratio = self._height / self.subject_number

        point_coordinates = np.array(self.log[key])

        point_coordinates[:, 1] = point_coordinates[:, 1] * height_frame_ratio

        point_coordinates = np.concatenate([point_coordinates, [[self.frames, 0]]])
        point_coordinates[:, 0] = point_coordinates[:, 0] * width_frame_ratio
        return point_coordinates

    def redraw_verts(self):
        asymptomatic_points = self.get_area_chart_strip("ASYMPTOMATIC")
        infected_points = self.get_area_chart_strip("INFECTED")
        immune_points = self.get_area_chart_strip("IMMUNE")

        immune_points[:, 1] = self._height - (immune_points[:, 1] + infected_points[:, 1] + asymptomatic_points[:, 1])

        infected_points[:, 1] = self._height - (infected_points[:, 1] + asymptomatic_points[:, 1])
        asymptomatic_points[:, 1] = self._height - asymptomatic_points[:, 1]

        #immune_points[:, 1] = infected_points[:, 1] + infected_points[:, 1] - immune_points[:, 1]
        immune_points = immune_points.tolist()
        infected_points = infected_points.tolist()
        asymptomatic_points = asymptomatic_points.tolist()




        self.fig.create_polygon(immune_points,
                                fill=self.theme.immune,
                                #fill=self.theme.area_plot_bg,
                                #width=3
                                )

        self.fig.create_polygon(infected_points,
                                fill=self.theme.infected,
                                # fill=self.theme.area_plot_bg,
                                # width=3
                                )
        self.fig.create_polygon(asymptomatic_points,
                                fill=self.theme.asymptomatic,
                                # fill=self.theme.area_plot_bg,
                                # width=3
                                )
    def observe(self, observable):
        observable.attach(self)