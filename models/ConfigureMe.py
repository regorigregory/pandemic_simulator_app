from enum import Enum


class InfectionStatuses(Enum):
    SUSCEPTIBLE = 0
    INFECTED = 1
    IMMUNE = 2


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
            self.one = "#F26627"
            self.two = "#F9A26C"
            self.three = "#EFEEEE"
            self.four = "#9BD7D1"
            self.five = "#325D79"

            self.button_attributes = {"bg": self.one, "fg": self.three, "width": 30, "pady": 5, "padx": 5}
            self.scenario_attributes = {"bg": self.four, "fg": self.three, "width": 15, "pady": 5, "padx": 5}
            self.default_bg = "white"
            self.area_plot_bg = "#D3BCCC"
            self.area_plot_colours = ["#4A306D", "#0E273C"]

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
                                              [1, 500]]

            self.general["SUBJECT_VELOCITY_RANGE_MAX"] = ["Scale", "The maximum movement speed of a subject:", [1, 10]]

            self.general["INITIAL_INFECTION_RATIO"] = ["Scale",
                                                       "The ratio of the initially infected subjects:",
                                                       [0, 1]]

            self.general["INFECTION_RADIUS"] = ["Scale", "Infection radius around a subject in pixels:", [1, 100]]
            self.general["CHANCE_OF_INFECTION"] = ["Scale",
                                                   "Infection chance per each day:",
                                                   [0, 1]]

            self.general["SUBJECT_SIZE"] = ["Scale", "Subject size (radius) in pixels:", [1, 15]]





            self.general["RECOVERY_TIME_RANGE_MIN"] = ["Scale",
                                              "Minimum recovery time (days):",
                                                  [0,100]]

            self.general["RECOVERY_TIME_RANGE_MAX"] = ["Scale",
                                              "Maximum recovery time (days):",
                                                  [0,100]]

            self.general["INCUBATION_PERIOD_RANGE_MIN"] = ["Scale",
                                                       "Minimum recovery time (days):",
                                                       [0, 100]]

            self.general["INCUBATION_PERIOD_RANGE_MAX"] = ["Scale",
                                                           "Maximum recovery time (days):",
                                                           [0, 100]]

            self.general["SUBJECT_COMPLIANCE"] = ["Scale",
                                              "What ratio of subjects comply with restrictions:",
                                                  [0, 1]]

            self.general["DAYS_PER_SECOND"] = ["Scale",
                                           "Days per second:",
                                               [1, 100]]

            self.general["LOCKDOWN_AFTER"] = ["Scale",
                                              "Start of the lockdown after the first infection (days):",
                                              [0, 100]]
            self.general["ASYMPTOMATIC_RATIO"] = ["Scale",
                                                     "The ratio of infected subjects who are asymptomatic (won't be moved to quarantine):",
                                                     [0, 1]]
            self.quarantine["QUARANTINE_AFTER"] = ["Scale",
                                                   "Subject moves into quarantine after this amount of days after the infection:",
                                                   [1, 30]]




            self.central["CENTRAL_VISIT_CHANCE"] = ["Scale",
                                            "Travelling chance to central location:",
                                            [0, 1]]


            self.central["CENTRAL_SUBJECT_NUMBER"] = ["Scale",
                                              "The number of subjects:",
                                              [0,500]]

            self.communities["COMMUNITIES_VISIT_CHANCE"] = ["Scale",
                                                "Travelling chance between communities:",
                                                [0,1]]

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
            self.NUMBER_OF_THREADS = 3
            self.SUBJECT_NUMBER = 300

            self.SUBJECT_VELOCITY_RANGE = [-1, 1]

            self.INITIAL_INFECTION_RATIO = 0.5
            self.INFECTION_RADIUS = 15
            self.CHANCE_OF_INFECTION = 0.8

            self.SUBJECT_SIZE = 5

            self.RECOVERY_TIME_RANGE = [50, 100]
            self.INCUBATION_PERIOD_RANGE = [2, 10]

            self.SUBJECT_COMPLIANCE = 1

            self.DAYS_PER_SECOND = 1

            self.QUARANTINE_AFTER = 0
            self.ASYMPTOMATIC_RATIO = 1
            self.LOCKDOWN_AFTER = 0
            self.CENTRAL_VISIT_CHANCE = 1
            self.CENTRAL_SUBJECT_NUMBER = 100

            self.COMMUNITIES_VISIT_CHANCE = 1
            self.COMMUNITIES_SUBJECT_PER = 100

            self.SOCIAL_DISTANCING = False
            self.QUARANTINE_MODE = False
            self.LOCKDOWN_MODE = False

            self.SUBJECT_TYPE = SubjectTypes.SUBJECT

            # Layout configuration

            self.MAIN_CANVAS_SIZE = [1024, 1024]

            self.DPI = 96
            self.DEFAULT_BG = Theme().default_bg

            self.COLUMNS_RATIO = 0.4

            self.SIMULATION_DIM = 0.4
            self.HEADER_DIM = 0.1
            self.GRAPH_DIM = 0.3

            self.FRAME_PADDING = dict(padx = 10, pady = 10)

            self.PARAMETERS_DIM = 0.8
            self.BUTTONS_DIM = 0.1
            self.SCENARIO_DIM = 0.1
            self.STATS_DIM = 0.1

            # scenario and buttons config

            self.BUTTONS_CONFIG = {"PAUSE": dict(text="Pause", **Theme().button_attributes),
                                   "RESET": dict(text="Reset", **Theme().button_attributes)}

            self.SCENARIO_CONFIG = {"SIMPLE": dict(text="Simple", **Theme().scenario_attributes),
                                    "CENTRAL": dict(text="Central Location", **Theme().scenario_attributes),
                                    "COMMUNITIES": dict(text="Communities", **Theme().scenario_attributes)}
            self.GRID_KWARGS = dict()
            self.GRID_KWARGS["MasterHeaderFrame"] = dict(row=0, column=0, columnspan=2, sticky="we")
            self.GRID_KWARGS["MasterLeftFrame"] = dict(row=1, column=0, sticky="nwe")
            self.GRID_KWARGS["MasterRightFrame"] = dict(row=1, column=1, sticky="nwe")

            self.GRID_KWARGS["GraphFrame"] = dict(row=0, column=0)
            self.GRID_KWARGS["StatsFrame"] = dict(row=1, column=0)

            self.GRID_KWARGS["SimulationFrame"] = dict(row=2, column=0)
            self.GRID_KWARGS["ButtonsFrame"] = dict(row=3, column=0)
            self.GRID_KWARGS["ScenarioFrame"] = dict(row=0, column=0)
            self.GRID_KWARGS["ParametersFrame"] = dict(row=1, column=0)
            self.PARAMETERS_UI_SETTINGS = SimulationParametersUIConfig()

    def __setattr__(self, key, value):
        if("VELOCITY_MAX" in key):
            value = [-value, value]
            key = key[0:-3] + "RANGE"

        elif("MIN" in key or "MAX" in key):
            index = 0 if "MIN" in key else 1
            key = key[0:-4]
            val = super().__getattribute__(key)
            val[index] = value
            if val[0] > value[1] or val[1] < val[0]:
                val[1-index] = val[index]
            value = val

        super().__setattr__(key, value)

    def get_main_canvas_size_tkinter(self):
        return "{}x{}".format(self.MAIN_CANVAS_SIZE[0], self.MAIN_CANVAS_SIZE[1])

    def get_header_frame_dimensions(self):
        return [self.MAIN_CANVAS_SIZE[0], self.HEADER_FRAME_HEIGHT]

    def get_main_subjects_box_dimensions(self):
        max_x, max_y = self.get_dimensions(1, "SIMULATION_DIM")
        return [[0, max_x], [0, max_y]]

    def get_dimensions(self, column, key):

        if column == 0:
            col_ratio = 1
        else:
            col_ratio = self.COLUMNS_RATIO if column == 1 else 1 - self.COLUMNS_RATIO
        if column == 2:
            say_hi = 1
        col_width = col_ratio * self.MAIN_CANVAS_SIZE[0]
        row_ratio = getattr(self, key)
        row_height = row_ratio * self.MAIN_CANVAS_SIZE[1]
        return [int(col_width), int(row_height)]
