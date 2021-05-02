
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
        self.fig = tk.Frame(root, bg=self.theme.default_bg)
        self.second_row = tk.Frame(self.fig, bg=self.theme.default_bg)
        self.second_row.grid(row=3, column=0, sticky="we", columnspan=3)

        self.data_label = dict(DAY = tk.Label(self.fig, text ="Day",**self.theme.label_data),
                               R_RATE=tk.Label(self.fig, text="R-rate", **self.theme.label_data),
                               R_GROWTH=tk.Label(self.fig, text="R-growth-rate", **self.theme.label_data),
                               ASYMPTOMATIC=tk.Label(self.second_row, text = "Asymptomatic", **self.theme.label_data),
                               INFECTED=tk.Label(self.second_row, text = "Infected", **self.theme.label_data),
                               SUSCEPTIBLE=tk.Label(self.second_row, text = "Susceptible", **self.theme.label_data),
                               IMMUNE= tk.Label(self.second_row, text = "Immune", **self.theme.label_data)
                               )
        self.data_value = dict(DAY=tk.Label(self.fig, text="-", **self.theme.label_value),
                               R_RATE=tk.Label(self.fig, text="-", **self.theme.label_value),
                               R_GROWTH=tk.Label(self.fig, text="-", **self.theme.label_value),
                               ASYMPTOMATIC=tk.Label(self.second_row, text="-", fg=self.theme.asymptomatic,  **self.theme.label_value),
                               INFECTED=tk.Label(self.second_row, text="-", fg=self.theme.infected, **self.theme.label_value),
                               SUSCEPTIBLE=tk.Label(self.second_row, text="-", fg=self.theme.susceptible, **self.theme.label_value),
                               IMMUNE=tk.Label(self.second_row, text="-",fg=self.theme.immune, **self.theme.label_value)
                               )

        column = 0
        for i, k, v in zip(range(len(self.data_value)), self.data_label.keys(), self.data_label.values()):
            if i == 3:
                column = 0
            v.grid(row=0, column=column, sticky="we")
            self.data_value[k].grid(row=1, column=column, sticky="we")
            column += 1

        self.fig.grid(row=1, column=0, sticky="nswe")


    def update_stats(self, data):
        self.subject_number = MainConfiguration().SUBJECT_NUMBER

        if data:
            for k, v in data.items():
                    self.data_value[k].configure({"text":len(v)})
        else:
            for v in self.data_value.values():
                v.configure({"text": "-"})


    def update(self, data):
        self.update_stats(data)


class TKAreaChart(Observer):
    def __init__(self, root=None):
        super().__init__()
        self.width, self.height = self.config.get_dimensions("GraphFrame")
        self.width = self.width - 3 * self.config.INNER_PADDING
        self.DPI = self.config.DPI
        self.frames = 0
        self.init_log()

        self.fig = tk.Canvas(root, width=self.width, height = self.height, bg = self.theme.susceptible)

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