from enum import Enum


class InfectionStatuses(Enum):
    SUSCEPTIBLE = 0
    INFECTED = 1
    IMMUNE = 2


class SubjectTypes(Enum):
    PARTICLE = 0,
    SUBJECT = 1

class Parameters(object):
    _shared_data = dict()
    instance = None

    def __new__(cls):

        if cls.instance is None:

            return super(Parameters, cls).__new__(cls)
        else:
            return cls.instance

    def __init__(self):

        if Parameters.instance is None:
            self.all = dict()
            self.simple = dict()
            self.quarantine = dict()
            self.lockdown = dict()
            self.central = dict()
            self.communities = dict()


            self.all["SUBJECT_VELOCITY_MIN"] = ["Scale", "The minimum movement speed of a subject:", [0, 1]]
            self.all["SUBJECT_VELOCITY_MAX"] = ["Scale", "The maximum movement speed of a subject:", [0, 1]]
            self.all["SUBJECT_SIZE"] = ["Scale", "Subject size (radius) in pixels:", [0, 15]]
            self.all["INFECTION_RADIUS"] = ["Scale", "Infection radius around a subject in pixels:", [0, 100]]

            self.all["CHANCE_OF_INFECTION"] = ["Scale",
                                               "Infection chance per each day:",
                                               [0,1]]
            self.all["INITIAL_INFECTION_RATIO"] = ["Scale",
                                                   "The ratio of the initially infected subjects:",
                                                   [0,1]]

            self.all["INFECTION_MIN_SPAN"] = ["Scale",
                                              "Minimum recovery time (days):",
                                              [0,100]]

            self.all["INFECTION_MAX_SPAN"] = ["Scale",
                                              "Maximum recovery time (days):",
                                              [0,100]]

            self.all["SUBJECT_COMPLIANCE"] = ["Scale",
                                              "What ratio of subjects comply with restrictions:",
                                              [0, 1]]

            self.all["DAYS_PER_SECOND"] = ["Scale",
                                           "Days per second:",
                                           [1, 100]]


            self.simple["SUBJECT_NUMBER"] = ["Scale",
                                             "The number of subjects:",
                                             [1, 500]]

            self.quarantine["QUARANTINE_AFTER"] = ["Scale",
                                                   "Incubation period (subject moves into quarantine after this amount of days):",
                                                   [1, 30]]

            self.quarantine["ASYMPTOMATIC_RATIO"] = ["Scale",
                                                   "The ratio of infected subjects who are asymptomatic (won't be moved to quarantine):",
                                                     [0, 1]]

            self.lockdown["LOCKDOWN_AFTER"] = ["Scale",
                                               "Start of the lockdown after the first infection (days):",
                                               [1, 100]]

            self.central["VISIT_CHANCE"] = ["Scale",
                                            "Travelling chance to central location:",
                                            [0, 1]]
            self.central["SUBJECT_NUMBER"] = ["Scale",
                                              "The number of subjects:",
                                              [0,500]]

            self.communities["VISIT_CHANCE"] = ["Scale",
                                                "Travelling chance between communities:",
                                                [0,1]]

            self.communities["INDIVIDUALS_PER_COMMUNITY"] = ["Scale",
                                                             "Travelling chance between communities:",
                                                             [0, 100]]


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
            self.scenario_attributes = {"bg": self.four, "fg": self.three, "width": 30, "pady": 5, "padx": 5}
            self.default_bg = "white"

class Constants(object):
    _shared_data = dict()
    instance = None

    def __new__(cls):
        if cls.instance is None:
            return super(Constants, cls).__new__(cls)
        else:
            return cls.instance

    def __init__(self):
        if Constants.instance is None:
            Constants.instance = self
            Constants.instance.__dict__ = Constants._shared_data

            self.NUMBER_OF_THREADS = 3
            self.NUMBER_OF_SUBJECTS = 1000

            self.INITIAL_INFECTED_SUBJECTS_RATIO = 0.1
            self.INFECTION_RADIUS = 15
            self.PARTICLE_RADIUS = 5

            self.RECOVERY_TIME = [50, 100]
            self.INCUBATION_PERIOD = [2, 10]

            self.INFECTION_PROBABILITY_PER_TIME_PERIOD = [0.6, 0.8]

            self.SOCIAL_DISTANCE_FACTOR = 0

            self.MAIN_CANVAS_SIZE = [1024, 1024]

            self.COLUMNS_RATIO = 0.4
            self.SIMULATION_DIM = 0.4
            self.HEADER_DIM = 0.1
            self.GRAPH_DIM = 0.3
            self.FRAME_PADDING = dict(padx = 10, pady = 10)
            self.PARAMETERS_DIM = 0.5
            self.BUTTONS_DIM = 0.1
            self.SCENARIO_DIM = 0.1
            self.STATS_DIM = 0.1

            # layout grid config
            self.GRID_KWARGS = {}
            self.GRID_KWARGS["MasterHeaderFrame"] = dict(row=0, column=0, columnspan=2, sticky="we")
            self.GRID_KWARGS["MasterLeftFrame"] = dict(row=1, column=0, sticky="we")
            self.GRID_KWARGS["MasterRightFrame"] = dict(row=1, column=1, sticky="we")

            self.GRID_KWARGS["GraphFrame"] = dict(row=0, column=0)
            self.GRID_KWARGS["SimulationFrame"] = dict(row=1, column=0)
            self.GRID_KWARGS["ButtonsFrame"] = dict(row=2, column=0)
            self.GRID_KWARGS["ScenarioFrame"] = dict(row=1, column=0)
            self.GRID_KWARGS["ParametersFrame"] = dict(row=2, column=0)
            self.GRID_KWARGS["StatsFrame"] = dict(row=0, column=0)


            self.VELOCITY_RANGE = [[-1, 1],
                                   [-1, 1]]
            self.ACCELERATION_RANGE = [[1, 1], [1, 1]]
            self.DPI = 96
            self.SOCIAL_DISTANCING = False

            self.SUBJECT_TYPE = SubjectTypes.SUBJECT

            self.BUTTONS_CONFIG = {"START": dict(text="Start", **Theme().button_attributes),
                                   "PAUSE": dict(text="Pause", **Theme().button_attributes),
                                   "RESET": dict(text="Reset", **Theme().button_attributes)}

            self.SCENARIO_CONFIG = {"START": dict(text="Simple", **Theme().scenario_attributes),
                                   "PAUSE": dict(text="Central Location", **Theme().scenario_attributes),
                                   "RESET": dict(text="Communities", **Theme().scenario_attributes)}

            self.PARAMETERS = Parameters()
            self.DEFAULT_BG = Theme().default_bg

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
            col_ratio = self.COLUMNS_RATIO if column == 1 else 0.8 - self.COLUMNS_RATIO

        col_width = col_ratio * self.MAIN_CANVAS_SIZE[0]
        row_ratio = getattr(self, key)
        row_height = row_ratio * self.MAIN_CANVAS_SIZE[1]
        return [int(col_width), int(row_height)]
