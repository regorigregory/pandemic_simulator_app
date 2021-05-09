import tkinter as tk
from enum import Enum

import numpy as np


class InfectionStatuses(Enum):
    SUSCEPTIBLE = 0
    ASYMPTOMATIC = 1
    INFECTED = 2
    IMMUNE = 3


class SubjectTypes(Enum):
    PARTICLE = 0,
    SUBJECT = 1


class Theme(object):
    _shared_data = dict()
    instance = None

    def __new__(cls):

        if cls.instance is None:
            return super(Theme, cls).__new__(cls)
        else:
            return cls.instance

    def __init__(self):

        if Theme.instance is None:
            self.one = "#03A0D3"
            self.two = "#CC1F7F"
            self.three = "#EFEEEE"
            self.four = "#9BD7D1"
            self.five = "#21213D"

            self.button_attributes = {"bg": self.two, "fg": self.three, "width": 30, "pady": 5, "padx": 5}
            self.scenario_attributes = {"bg": self.one, "fg": self.three, "width": 15, "pady": 5, "padx": 5}
            self.checkbox_attributes = {"bg": self.five, "fg": self.three, "width": 15, "pady": 5, "padx": 5,
                                        "selectcolor": self.two}
            self.darkest_bg = "#000405"
            self.default_bg = "#0B1A1A"
            self.default_text = "white"

            self.label_data = dict(bg=self.default_bg, fg=self.default_text, width=20, pady=3, padx=3)
            self.label_value = dict(bg=self.default_bg, font=("Courier", 26), width=8, pady=3, padx=4)
            self.header_text_kwargs = dict(fg="#95AFA2", bg=self.darkest_bg, font=("Roboto", 16), pady=4, padx=15)
            self.plot_bg = self.default_bg
            self.infected = "#CC1F7F"
            self.asymptomatic = "#E58342"
            self.susceptible = "#03A0D3"  # "#E6C645"
            self.immune = "#999999"


class SimulationParametersUIConfig(object):
    _shared_data = dict()
    instance = None

    def __new__(cls):

        if cls.instance is None:

            return super(SimulationParametersUIConfig, cls).__new__(cls)
        else:
            return cls.instance

    def __init__(self):

        if SimulationParametersUIConfig.instance is None:
            self.constants = dict()
            self.live = dict()

            self.constants["SUBJECT_NUMBER"] = ["Scale",
                                              "The number of subjects:",
                                                [1, 300]]

            self.constants["SUBJECT_INITIAL_INFECTION_RATIO"] = ["Scale",
                                                               "The ratio of the initially infected subjects:",
                                                                 [0, 1]]

            self.constants["SUBJECT_INCUBATION_PERIOD"] = ["Scale",
                                                           "Incubation period (days):",
                                                           [0, 100]]

            self.constants["SUBJECT_RECOVERY_TIME"] = ["Scale",
                                                     "Recovery time (days):",
                                                       [0, 100]]

            self.live["SUBJECT_COMPLIANCE"] = ["Scale",
                                                  "What ratio of subjects comply with restrictions:",
                                                    [0, 1]]

            self.live["DAYS_PER_MINUTE"] = ["Scale",
                                               "Days per minute (~):",
                                                 [1, 120]]
            self.live["SUBJECT_VELOCITY_MULTIPLIER"] = ["Scale",
                                                "Movement speed multiplier:", [1, 100]]


            self.live["SUBJECT_SIZE"] = ["Scale", "Subject size (radius) in pixels:", [1, 5]]

            self.live["SUBJECT_INFECTION_RADIUS"] = ["Scale", "Infection radius around a subject in pixels:",
                                                          [1, 10]]
            self.live["SUBJECT_CHANCE_OF_INFECTION"] = ["Scale",
                                                           "Infection chance per each day:",
                                                             [0, 1]]

            self.live["COMMUNITIES_VISIT_CHANCE"] = ["Scale",
                                                        "Travelling chance between communities:",
                                                          [0, 1]]


class MainConfiguration(object):
    _shared_data = dict()
    instance = None

    def __new__(cls):
        if cls.instance is None:
            return super(MainConfiguration, cls).__new__(cls)
        else:
            return cls.instance

    def __init__(self):

        if MainConfiguration.instance is None:
            MainConfiguration.instance = self
            MainConfiguration.instance.__dict__ = MainConfiguration._shared_data
            self.load_defaults()
            # general settings

            self.APPLICATION_TITLE = "Pandemic simulator"
            self.SOCIAL_DISTANCING_MODE = False
            self.QUARANTINE_MODE = False
            self.LOCKDOWN_MODE = False
            self.COMMUNITY_MODE = False

            self.QUARANTINE_AFTER = 0
            self.LOCKDOWN_AFTER = 0
            self.QUARANTINE_APPROACHING_SPEED = 500
            self.COUNT_R_RATE = True
            # subject settings
            self.SUBJECT_VELOCITY=10
            self.SUBJECT_TYPE = SubjectTypes.SUBJECT



            # Communities settings

            self.COMMUNITIES_ROWS = 3
            self.COMMUNITIES_COLUMNS = 3


            # Layout configuration

            self.MAIN_CANVAS_SIZE = [1024, 1024]
            self.INNER_PADDING = 15
            self.QUARANTINE_WIDTH = 0.1
            self.DPI = 96
            self.DEFAULT_BG = Theme().default_bg
            self.FRAME_PADDING = dict(padx=10, pady=10)

            self.COLUMNS_RATIO = [0.45, 0.50]

            self.GRID_SETTINGS = dict()

            self.GRID_SETTINGS["MasterLeftFrame"] = dict(height=0.9, column=0,
                                                         grid_kwargs=dict(row=0, column=0, sticky="nwes"))

            self.GRID_SETTINGS["MasterRightFrame"] = dict(height=0.9, column=1,
                                                          grid_kwargs=dict(row=0, column=1, sticky="nwes"))

            self.GRID_SETTINGS["StatsFrame"] = dict(height=0.3, column=1,
                                                    grid_kwargs=dict(row=1, column=0, sticky="we"))

            self.GRID_SETTINGS["GraphFrame"] = dict(height=0.15, column=1,
                                                    grid_kwargs=dict(row=2, column=0, sticky="we"))

            self.GRID_SETTINGS["SimulationFrame"] = dict(height=0.394, column=1,
                                                         grid_kwargs=dict(row=0, column=0))

            self.GRID_SETTINGS["ScenarioFrame"] = dict(height=0.1, column=0,
                                                       grid_kwargs=dict(row=1, column=0))

            self.GRID_SETTINGS["ConstantsParametersFrame"] = dict(height=0.25, column=0,
                                                         grid_kwargs=dict(row=0, column=0))

            self.GRID_SETTINGS["LiveParametersFrame"] = dict(height=0.4, column=0,
                                                                grid_kwargs=dict(row=2, column=0))

            self.PARAMETERS_UI_SETTINGS = SimulationParametersUIConfig()

            # scenario and buttons config

            self.BUTTONS_CONFIG = {"START": dict(text="Start", **Theme().button_attributes),
                                   "STOP": dict(text="Stop", **Theme().button_attributes),
                                   "RESET": dict(text="Reset settings", **Theme().button_attributes)}

            self.SCENARIO_CONFIG = {"SIMPLE": ["Button", dict(text="Simple", **Theme().scenario_attributes)],
                                    "CENTRAL": ["Button", dict(text="Central Location", **Theme().scenario_attributes)],
                                    "COMMUNITIES": ["Button", dict(text="Communities", **Theme().scenario_attributes)]}

            self.CHECKBOX_CONFIG = {"SOCIAL_DISTANCING_MODE":
                                        ["Checkbutton", dict(text="Social distancing",
                                                             name="SOCIAL_DISTANCING_MODE".lower(),
                                                             **Theme().checkbox_attributes)],

                                    "QUARANTINE_MODE": ["Checkbutton", dict(text="Quarantine",
                                                                            name="QUARANTINE_MODE".lower(),
                                                                            **Theme().checkbox_attributes)],
                                    "COMMUNITY_MODE": ["Checkbutton",
                                                       dict(text="Community mode",
                                                            name="COMMUNITY_MODE".lower(),
                                                            **Theme().checkbox_attributes)]
                                    }

            self.STATS_CONFIG = dict(LABEL_KWDS=dict(bg=Theme().default_bg),
                                     VALUE_KWDS=dict(bg=Theme().default_bg))

    def load_defaults(self):
        with open("./models/default_settings", "r") as f:
            for line in f.readlines():
                key, type,  value = line.split(":")
                if type == "int":
                    value = int(value)
                else:
                    value = float(value)
                setattr(self, key, value)

    def __getattr__(self, item):
        temp = super().__getattribute__(item)
        if isinstance(temp, tk.BooleanVar):
            return temp.get()
        else:
            return item

    def __setattr__(self, key, value):
        if key == "SUBJECT_VELOCITY":
            value = [-value, value]

        """elif "MIN" in key or "MAX" in key:
            index = 0 if "MIN" in key else 1
            key = key[0:-4]
            val = super().__getattribute__(key)
            val[index] = value
            if val[0] > val[1] or val[1] < val[0]:
                val[1 - index] = val[index]
            value = val"""

        super().__setattr__(key, value)

    def get_frame_dimensions_of(self, key):
        sett = self.GRID_SETTINGS[key]
        row_ratio = sett["height"]
        column_ratio = self.COLUMNS_RATIO[sett["column"]]

        col_width = column_ratio * self.MAIN_CANVAS_SIZE[0]

        row_height = row_ratio * self.MAIN_CANVAS_SIZE[1]
        return [int(col_width), int(row_height)]

    def get_quarantine_dimensions(self):
        plot_dimensions = self.get_frame_dimensions_of("SimulationFrame")
        dimensions = dict()
        dimensions["x"] = self.INNER_PADDING
        dimensions["y"] = self.INNER_PADDING
        dimensions["width"] = plot_dimensions[0] * self.QUARANTINE_WIDTH
        dimensions["height"] = plot_dimensions[1] - 2 * self.INNER_PADDING

        return dimensions

    def get_main_canvas_size_tkinter(self):
        return "{}x{}".format(self.MAIN_CANVAS_SIZE[0], self.MAIN_CANVAS_SIZE[1])

    def get_simulation_canvas_total_bounds(self):
        max_x, max_y = self.get_frame_dimensions_of("SimulationFrame")
        return [[0, max_x], [0, max_y]]

    def get_particle_movement_canvas_bounds(self):
        canvas_dims = self.get_simulation_canvas_total_bounds()
        if (isinstance(self.QUARANTINE_MODE, bool) and self.QUARANTINE_MODE) or (not isinstance(self.QUARANTINE_MODE, bool) and self.QUARANTINE_MODE.get()):
            q_dims = self.get_quarantine_dimensions()
            canvas_dims[0][0] = q_dims["x"] + q_dims["width"]
        return np.array(canvas_dims)

    def get_particle_movement_border_bounds(self):
        canvas_dims = self.get_particle_movement_canvas_bounds()
        canvas_dims[:, 0] += self.INNER_PADDING
        canvas_dims[:, 1] -= self.INNER_PADDING
        return canvas_dims

    def get_particle_movement_bounds(self):
        canvas_dims = self.get_particle_movement_border_bounds()
        canvas_dims[:, 0] += self.SUBJECT_SIZE
        canvas_dims[:, 1] -= self.SUBJECT_SIZE
        return canvas_dims

    def get_particle_quarantine_position_boundaries(self):
        q_dims = self.get_quarantine_dimensions()
        subject_radius = self.SUBJECT_SIZE
        return [[q_dims["x"] + subject_radius, q_dims["x"] + q_dims["width"] - subject_radius],
                [q_dims["y"] + subject_radius, q_dims["y"] + q_dims["height"] - subject_radius]]

    def get_community_cells_border_bounds(self):
        config = self
        main_dimensions = config.get_particle_movement_border_bounds()
        full_width = main_dimensions[0][1] - main_dimensions[0][0]
        x_start = main_dimensions[0][0]

        full_height = main_dimensions[1][1]
        padding = config.INNER_PADDING
        rows = config.COMMUNITIES_ROWS
        columns = config.COMMUNITIES_COLUMNS
        row_height = full_height / rows
        column_width = full_width / columns
        patch_dimensions = dict(width=column_width - padding, height=row_height - padding)

        cells = []
        for row in range(rows):
            for column in range(columns):
                x = x_start + padding + column * column_width
                y = padding + row * row_height
                width = patch_dimensions["width"]
                height = patch_dimensions["height"]
                cells.append([[x, x + width], [y, y + height]])
        return cells

    def get_frames_per_day(self):
        return (60 / self.DAYS_PER_MINUTE) * self.FRAMES_PER_SECOND
