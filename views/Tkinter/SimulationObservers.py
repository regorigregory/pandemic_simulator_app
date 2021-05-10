import tkinter as tk
import numpy as np

from models.ConfigureMe import Theme, MainConfiguration
from views.AbstractClasses import Observer


class TKStats(Observer):
    def __init__(self, root):
        super().__init__()
        self.init_log()
        self.width, self.height = MainConfiguration().get_frame_dimensions_of("StatsFrame")
        self.fig = tk.Frame(root, bg=self.theme.default_bg, pady= 20)
        self.second_row = tk.Frame(self.fig, bg=self.theme.default_bg)
        self.second_row.grid(row=3, column=0, sticky="we", columnspan=3)

        self.data_label = dict(DAY=tk.Label(self.fig, text="Day", **self.theme.label_data),
                               R_RATE=tk.Label(self.fig, text="R-rate", **self.theme.label_data),
                               R_GROWTH=tk.Label(self.fig, text="R-growth-rate", **self.theme.label_data),
                               ASYMPTOMATIC=tk.Label(self.second_row, text="Asymptomatic", **self.theme.label_data),
                               INFECTED=tk.Label(self.second_row, text="Infected", **self.theme.label_data),
                               SUSCEPTIBLE=tk.Label(self.second_row, text="Susceptible", **self.theme.label_data),
                               IMMUNE=tk.Label(self.second_row, text="Immune", **self.theme.label_data)
                               )
        self.data_value = dict(DAY=tk.Label(self.fig, text="-", fg=self.theme.default_text, **self.theme.label_value),
                               R_RATE=tk.Label(self.fig, text="-",fg=self.theme.default_text, **self.theme.label_value),
                               R_GROWTH=tk.Label(self.fig, text="-",fg=self.theme.default_text, **self.theme.label_value),
                               ASYMPTOMATIC=tk.Label(self.second_row, text="-", fg=self.theme.asymptomatic,
                                                     **self.theme.label_value),
                               INFECTED=tk.Label(self.second_row, text="-", fg=self.theme.infected,
                                                 **self.theme.label_value),
                               SUSCEPTIBLE=tk.Label(self.second_row, text="-", fg=self.theme.susceptible,
                                                    **self.theme.label_value),
                               IMMUNE=tk.Label(self.second_row, text="-", fg=self.theme.immune,
                                               **self.theme.label_value)
                               )

        column = 0
        for i, k, v in zip(range(len(self.data_value)), self.data_label.keys(), self.data_label.values()):
            if i == 3:
                column = 0
            v.grid(row=0, column=column, sticky="we")
            self.data_value[k].grid(row=1, column=column, sticky="we")
            column += 1

        self.fig.grid(row=1, column=0, sticky="we")

    def update_stats(self, data):
        self.subject_number = MainConfiguration().SUBJECT_NUMBER

        if data:
            for k, v in data.items():
                if k == "R_GROWTH":
                    stop = True
                data = len(v) if isinstance(v, set) or isinstance(v, list) else v

                self.data_value[k].configure({"text": data})
        else:
            for v in self.data_value.values():
                v.configure({"text": "-"})

    def update(self, data):
        self.update_stats(data)


class TKAreaChart(Observer):
    def __init__(self, root=None):
        super().__init__()
        self.width, self.height = MainConfiguration().get_frame_dimensions_of("GraphFrame")
        self.width = self.width - 3 * MainConfiguration().INNER_PADDING
        self.DPI = MainConfiguration().DPI
        self.frames = 0
        self.init_log()
        self.y_axis_width = 50
        self.are_chart_height = self.height-20
        self.fig = tk.Canvas(root,
                             width=self.width - self.y_axis_width,
                             height=self.are_chart_height,
                             bg=self.theme.default_bg,
                             highlightthickness=0,
                             bd=0,
                             relief='ridge')

        self.init_area_chart()

        self.y_axis = tk.Canvas(root,
                                width=self.y_axis_width,
                                height=self.height,
                                bg=self.theme.default_bg,
                                highlightthickness=0,
                                bd=0,
                                relief='ridge')

        self.init_y_axis()

    def init_y_axis(self):
        offset = 10

        ax_height = self.height - offset * 2
        self.y_axis.create_line(0, offset, 0, self.height - offset, fill=self.theme.infected)

        for f in [1, 0.75, 0.5, 0.25, 0]:

            self.y_axis.create_text(30, offset + (1-f)*ax_height, text="{:.0f}%".format(f*100), fill=self.theme.infected)

            self.y_axis.create_line(0, offset + (1-f) * ax_height, 10, offset + (1-f) * ax_height, fill=self.theme.infected)


    def init_area_chart(self):
        self.fig.create_line(0, self.are_chart_height - 1, self.width - self.y_axis_width,
                             self.are_chart_height - 1,
                             fill=self.theme.infected)
        self.fig.create_line(0, (self.are_chart_height - 1)/2, self.width - self.y_axis_width,
                             (self.are_chart_height - 1)/2,
                             fill=self.theme.infected, dash=(4,2))
        self.fig.create_line(0, 0, self.width - self.y_axis_width,
                             0,
                             fill=self.theme.infected, dash=(4, 2))
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
            self.init_area_chart()

        else:
            self.frames += 1
            self.update_logs(new_data)
            self.fig.delete("all")
            self.init_area_chart()
            self.redraw_verts()

    def get_area_chart_strip(self, key):
        width_frame_ratio = self._width / self.frames
        height_frame_ratio = self.are_chart_height / self.subject_number

        point_coordinates = np.array(self.log[key])

        point_coordinates[:, 1] = point_coordinates[:, 1] * height_frame_ratio

        point_coordinates = np.concatenate([point_coordinates, [[self.frames, 0]]])
        point_coordinates[:, 0] = point_coordinates[:, 0] * width_frame_ratio
        return point_coordinates

    def redraw_verts(self):
        asymptomatic_points = self.get_area_chart_strip("ASYMPTOMATIC")
        infected_points = self.get_area_chart_strip("INFECTED")
        immune_points = self.get_area_chart_strip("IMMUNE")

        immune_points[:, 1] = self.are_chart_height - (immune_points[:, 1] + infected_points[:, 1] + asymptomatic_points[:, 1])

        infected_points[:, 1] = self.are_chart_height - (infected_points[:, 1] + asymptomatic_points[:, 1])
        asymptomatic_points[:, 1] = self.are_chart_height - asymptomatic_points[:, 1]

        immune_points = immune_points.tolist()
        infected_points = infected_points.tolist()
        asymptomatic_points = asymptomatic_points.tolist()

        self.fig.create_polygon(immune_points,
                                fill=self.theme.immune,
                                # fill=self.theme.area_plot_bg,
                                # width=3
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
