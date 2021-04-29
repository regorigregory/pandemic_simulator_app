from enum import Enum
import tkinter as tk


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
            self.checkbox_attributes = {"bg": self.five, "fg": self.three, "width": 15, "pady": 5, "padx": 5}

            self.default_bg = "white"

            self.plot_bg = "#21213D"
            self.infected = "#CC1F7F"
            self.asymptomatic = "#E58342"
            self.susceptible = "#03A0D3" #"#E6C645"
            self.immune = "#666666"


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
            self.general = dict()
            self.simple = dict()
            self.quarantine = dict()
            self.lockdown = dict()
            self.central = dict()
            self.communities = dict()

            self.mode = ["general"]

            self.general["SUBJECT_NUMBER"] = ["Scale",
                                              "The number of subjects:",
                                              [1, 300]]
            self.general["DAYS_PER_SECOND"] = ["Scale",
                                               "Days per second:",
                                               [1, 300]]
            self.general["SUBJECT_VELOCITY"] = ["Scale", "The maximum movement speed of a subject:", [1, 10]]

            self.general["SUBJECT_INITIAL_INFECTION_RATIO"] = ["Scale",
                                                       "The ratio of the initially infected subjects:",
                                                       [0, 1]]

            self.general["SUBJECT_SIZE"] = ["Scale", "Subject size (radius) in pixels:", [1, 15]]

            self.general["SUBJECT_INFECTION_RADIUS"] = ["Scale", "Infection radius around a subject in pixels:", [1, 100]]
            self.general["SUBJECT_CHANCE_OF_INFECTION"] = ["Scale",
                                                   "Infection chance per each day:",
                                                   [0, 1]]

            self.general["SUBJECT_RECOVERY_TIME"] = ["Scale",
                                             "Recovery time (days):",
                                             [0, 100]]

            self.general["SUBJECT_INCUBATION_PERIOD"] = ["Scale",
                                                 "Incubation period (days):",
                                                 [0, 100]]

            self.general["SUBJECT_COMPLIANCE"] = ["Scale",
                                                  "What ratio of subjects comply with restrictions:",
                                                  [0, 1]]

            self.general["LOCKDOWN_AFTER"] = ["Scale",
                                              "Start of the lockdown after the first infection (days):",
                                              [0, 100]]
            self.general["ASYMPTOMATIC_RATIO"] = ["Scale",
                                                  "Asymptomatic patients (won't be moved to quarantine):",
                                                  [0, 1]]
            self.quarantine["QUARANTINE_AFTER"] = ["Scale",
                                                   "Subject moves into quarantine after this amount of days after the infection:",
                                                   [1, 30]]

            self.central["CENTRAL_VISIT_CHANCE"] = ["Scale",
                                                    "Travelling chance to central location:",
                                                    [0, 1]]

            self.central["CENTRAL_SUBJECT_NUMBER"] = ["Scale",
                                                      "The number of subjects:",
                                                      [0, 500]]

            self.communities["COMMUNITIES_VISIT_CHANCE"] = ["Scale",
                                                            "Travelling chance between communities:",
                                                            [0, 1]]

            self.communities["COMMUNITIES_SUBJECT_PER"] = ["Scale",
                                                           "Travelling chance between communities:",
                                                           [0, 100]]


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

            # general settings

            self.NUMBER_OF_THREADS = 3
            self.FRAME_MULTIPLIER = 5
            self.SOCIAL_DISTANCING_MODE = False
            self.QUARANTINE_MODE = False
            self.LOCKDOWN_MODE = False
            self.COMMUNITY_MODE = False
            # subject settings

            self.SUBJECT_NUMBER = 100
            self.SUBJECT_SIZE = 4
            self.SUBJECT_INITIAL_INFECTION_RATIO = 0.5
            self.SUBJECT_INFECTION_RADIUS = 15
            self.SUBJECT_CHANCE_OF_INFECTION = 0.8
            self.SUBJECT_RECOVERY_TIME = 30
            self.SUBJECT_INCUBATION_PERIOD = 15
            self.SUBJECT_COMPLIANCE = 1
            self.SUBJECT_VELOCITY = 1
            self.SUBJECT_TYPE = SubjectTypes.SUBJECT

            self.DAYS_PER_SECOND = 10

            self.QUARANTINE_AFTER = 0
            self.ASYMPTOMATIC_RATIO = 1
            self.LOCKDOWN_AFTER = 0
            self.CENTRAL_VISIT_CHANCE = 1
            self.CENTRAL_SUBJECT_NUMBER = 100
            self.QUARANTINE_APPROACHING_SPEED = 20

            # Communities settings

            self.COMMUNITIES_ROWS = 3
            self.COMMUNITIES_COLUMNS = 3

            self.COMMUNITIES_VISIT_CHANCE = 1
            self.COMMUNITIES_SUBJECT_PER = 100

            # Layout configuration

            self.MAIN_CANVAS_SIZE = [1024, 1024]
            self.INNER_PADDING = 10
            self.QUARANTINE_WIDTH = 0.1
            self.DPI = 96
            self.DEFAULT_BG = Theme().default_bg
            self.FRAME_PADDING = dict(padx=10, pady=10)

            self.COLUMNS_RATIO = [0.35, 0.6]

            # scenario and buttons config

            self.BUTTONS_CONFIG = {"PAUSE": dict(text="Pause", **Theme().button_attributes),
                                   "RESET": dict(text="Reset", **Theme().button_attributes)}

            self.SCENARIO_CONFIG = {"SIMPLE": ["Button", dict(text="Simple", **Theme().scenario_attributes)],
                                    "CENTRAL": ["Button", dict(text="Central Location", **Theme().scenario_attributes)],
                                    "COMMUNITIES": ["Button", dict(text="Communities", **Theme().scenario_attributes)]}

            self.CHECKBOX_CONFIG = {"SOCIAL_DISTANCING_MODE": ["Checkbutton", dict(text="Social distancing",
                                                                                   name="SOCIAL_DISTANCING_MODE".lower(),
                                                                                   **Theme().checkbox_attributes)],

                                    "QUARANTINE_MODE": ["Checkbutton", dict(text="Quarantine",
                                                                            name = "QUARANTINE_MODE".lower(),
                                                                            **Theme().checkbox_attributes)],
                                    "LOCKDOWN_MODE": ["Checkbutton",
                                                      dict(text="Lockdown",
                                                           name = "LOCKDOWN_MODE".lower(),
                                                           **Theme().checkbox_attributes)],
                                    "COMMUNITY_MODE": ["Checkbutton",
                                                      dict(text="Community mode",
                                                           name="COMMUNITY_MODE".lower(),
                                                           **Theme().checkbox_attributes)]
                                    }
            self.FRAME_SETTINGS = dict()
            self.FRAME_SETTINGS["MasterHeaderFrame"] = dict(height=0.1, column=0,
                                                            grid_kwargs=dict(row=0, column=0, columnspan=2,
                                                                             sticky="we"))

            self.FRAME_SETTINGS["MasterLeftFrame"] = dict(height=0.9, column=0,
                                                          grid_kwargs=dict(row=0, column=0, sticky="nwes"))

            self.FRAME_SETTINGS["MasterRightFrame"] = dict(height=0.9, column=1,
                                                           grid_kwargs=dict(row=0, column=1, sticky="nwes"))

            self.FRAME_SETTINGS["GraphFrame"] = dict(height=0.3, column=0,
                                                     grid_kwargs=dict(row=3, column=0))

            self.FRAME_SETTINGS["StatsFrame"] = dict(height=0.05, column=0,
                                                     grid_kwargs=dict(row=2, column=0))

            self.FRAME_SETTINGS["SimulationFrame"] = dict(height= 1, column=1,
                                                          grid_kwargs=dict(row=0, column=0))

            self.FRAME_SETTINGS["ButtonsFrame"] = dict(height=0.05, column=1,
                                                       grid_kwargs=dict(row=2, column=0))

            self.FRAME_SETTINGS["ScenarioFrame"] = dict(height=0.1, column=0,
                                                        grid_kwargs=dict(row=0, column=0))

            self.FRAME_SETTINGS["ParametersFrame"] = dict(height=0.5, column=0,
                                                          grid_kwargs=dict(row=1, column=0))

            self.PARAMETERS_UI_SETTINGS = SimulationParametersUIConfig()

    def __getattr__(self, item):
        temp = super().__getattribute__(item)
        if isinstance(temp, tk.BooleanVar):
            return temp.get()
        else:
            return item

    def __setattr__(self, key, value):
        if key == "SUBJECT_VELOCITY":
            value = [-value, value]

        elif "MIN" in key or "MAX" in key:
            index = 0 if "MIN" in key else 1
            key = key[0:-4]
            val = super().__getattribute__(key)
            val[index] = value
            if val[0] > val[1] or val[1] < val[0]:
                val[1 - index] = val[index]
            value = val

        super().__setattr__(key, value)

    def get_quarantine_dimensions(self):
        plot_dimensions = self.get_dimensions("SimulationFrame")
        dimensions = dict()
        dimensions["x"] = self.INNER_PADDING
        dimensions["y"] = self.INNER_PADDING
        dimensions["width"] = plot_dimensions[0] * self.QUARANTINE_WIDTH
        dimensions["height"] = plot_dimensions[1] - 2 * self.INNER_PADDING

        return dimensions

    def get_main_canvas_size_tkinter(self):
        return "{}x{}".format(self.MAIN_CANVAS_SIZE[0], self.MAIN_CANVAS_SIZE[1])

    def get_header_frame_dimensions(self):
        return [self.MAIN_CANVAS_SIZE[0], self.HEADER_FRAME_HEIGHT]

    def get_main_subjects_box_dimensions(self):
        max_x, max_y = self.get_dimensions("SimulationFrame")
        return [[0, max_x], [0, max_y]]

    def get_particle_position_boundaries(self):
        canvas_dims = self.get_main_subjects_box_dimensions()
        if self.QUARANTINE_MODE.get():
            q_dims = self.get_quarantine_dimensions()
            canvas_dims[0][0] = q_dims["x"] + q_dims["width"] + 1
        return canvas_dims

    def get_particle_quarantine_position_boundaries(self):
        q_dims = self.get_quarantine_dimensions()
        return [[q_dims["x"], q_dims["x"] + q_dims["width"]], [q_dims["y"], q_dims["y"] + q_dims["height"]]]

    def get_dimensions(self, key):
        sett = self.FRAME_SETTINGS[key]
        row_ratio = sett["height"]
        column_ratio = self.COLUMNS_RATIO[sett["column"]]

        col_width = column_ratio * self.MAIN_CANVAS_SIZE[0]

        row_height = row_ratio * self.MAIN_CANVAS_SIZE[1]
        return [int(col_width), int(row_height)]
