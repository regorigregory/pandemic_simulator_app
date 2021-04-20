from enum import Enum


class InfectionStatuses(Enum):
    SUSCEPTIBLE = 0
    INFECTED = 1
    IMMUNE = 2


class SubjectTypes(Enum):
    PARTICLE = 0,
    SUBJECT = 1

class Settings(object):
    _shared_data = dict()
    instance = None

    def __new__(cls):

        if cls.instance is None:

            return super(Theme, cls).__new__(cls)
        else:
            return cls.instance

    def __init__(self):

        if Settings.instance is None:
            self.all = dict()
            self.all["SUBJECT_VELOCITY_MIN"] = ["SLIDER", "The minimum movement speed of a subject:"]
            self.all["SUBJECT_VELOCITY_MAX"] = ["SLIDER", "The maximum movement speed of a subject:"]
            self.all["SUBJECT_SIZE"] = ["SLIDER", "Subject size (radius) in pixels:"]
            self.all["INFECTION_RADIUS"] = ["SLIDER", "Infection radius around a subject in pixels:"]

            self.all["CHANCE_OF_INFECTION"] = ["SLIDER", "Infection chance per each day:"]
            self.all["INITIAL_INFECTION_RATIO"] = ["SLIDER", "The ratio of the initially infected subjects:"]

            self.all["INFECTION_MIN_SPAN"] = ["SLIDER", "Minimum recovery time (days):"]
            self.all["INFECTION_MAX_SPAN"] = ["SLIDER", "Maximum recovery time (days):"]

            self.all["SOCIAL_DISTANCING_RATIO"] = ["SLIDER"]
            self.all["SUBJECT_COMPLIANCE"] = ["SLIDER"]

            self.all["DAYS_PER_SECOND"] = ["SLIDER"]

            self.simple["SUBJECT_NUMBER"] = ["SLIDER", "The number of subjects:"]

            self.quarantine["QUARANTINE_AFTER"] = ["SLIDER",
                                                   "Incubation period (subject moves into quarantine after this amount of days):"]
            self.quarantine["ASYMPTOMATIC_RATIO"] = ["SLIDER",
                                                   "The ratio of infected subjects who are asymptomatic (won't be moved to quarantine):"]

            self.lockdown["LOCKDOWN_AFTER"] = ["SLIDER", "Start of the lockdown after the first infection (days):"]

            self.central["VISIT_CHANCE"] = ["SLIDER", "Travelling chance to central location:"]
            self.central["SUBJECT_NUMBER"] = ["SLIDER", "The number of subjects:"]

            self.communities["VISIT_CHANCE"] = ["SLIDER", "Travelling chance between communities:"]
            self.communities["INDIVIDUALS_PER_COMMUNITY"] = ["SLIDER", "Travelling chance between communities:"]


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
            self.NUMBER_OF_SUBJECTS = 200

            self.INITIAL_INFECTED_SUBJECTS_RATIO = 0.2
            self.INFECTION_RADIUS = 40
            self.PARTICLE_RADIUS = 10

            self.RECOVERY_TIME = [50, 100]
            self.INCUBATION_PERIOD = [2, 10]

            self.INFECTION_PROBABILITY_PER_TIME_PERIOD = [0.5, 0.7]

            self.SOCIAL_DISTANCE_FACTOR = 0

            self.MAIN_CANVAS_SIZE = [1024, 768]

            self.COLUMNS_RATIO = 0.5
            self.SIMULATION_DIM = 0.6
            self.HEADER_DIM = 0.1
            self.GRAPH_DIM = 0.3
            self.FRAME_PADDING = dict(padx = 10, pady = 10)
            self.PARAMETERS_DIM = 0.6
            self.BUTTONS_DIM = 0.1
            self.SCENARIO_DIM = 0.1

            self.VELOCITY_RANGE = [[-10, 10],
                                   [-10, 10]]
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

    def get_main_canvas_size_tkinter(self):
        return "{}x{}".format(self.MAIN_CANVAS_SIZE[0], self.MAIN_CANVAS_SIZE[1])

    def get_header_frame_dimensions(self):
        return [self.MAIN_CANVAS_SIZE[0], self.HEADER_FRAME_HEIGHT]
    def get_main_subjects_box_dimensions(self):
        max_x, max_y = self.get_dimensions(1, "SIMULATION_DIM")
        return [[0, max_x], [0, max_y]]
    def get_dimensions(self, column, key):

        if column == -1:
            col_ratio = 1
        else:
            col_ratio = self.COLUMNS_RATIO if column == 0 else 1 - self.COLUMNS_RATIO
        col_width = col_ratio * self.MAIN_CANVAS_SIZE[0]
        row_ratio = getattr(self, key)
        row_height = row_ratio * self.MAIN_CANVAS_SIZE[1]
        return [int(col_width), int(row_height)]
