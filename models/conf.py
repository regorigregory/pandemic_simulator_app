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
        if(cls.instance == None):
            return super(Theme, cls).__new__(cls)
        else:
            return cls.instance
    def __init__(self):
        if(Theme.instance == None):
            self.one =  "#F26627"
            self.two = "#F9A26C"
            self.three = "#EFEEEE"
            self.four = "#9BD7D1"
            self.five = "#325D79"

            self.button_attributes = {}
            self.button_attributes["bg"] = self.one
            self.button_attributes["fg"] = self.three

            self.button_attributes["width"] = 50
            self.button_attributes["pady"] = 10

class Constants(object):
    _shared_data = dict()
    instance = None
    def __new__(cls):
        if(cls.instance == None):
            return super(Constants, cls).__new__(cls)
        else:
            return cls.instance
    def __init__(self):
        if(Constants.instance == None):
            Constants.instance = self
            Constants.instance.__dict__ = Constants._shared_data

            self.NUMBER_OF_THREADS = 2
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
            self.SIMULATION_DIM = 0.8
            self.HEADER_DIM = 0.1
            self.GRAPH_DIM = 0.3

            self.PARAMETERS_DIM = 0.6
            self.BUTTONS_DIM = 0.1
            self.SCENARIO_DIM = 0.1

            self.VELOCITY_RANGE = [[-10, 10],
                              [-10, 10]]
            self.ACCELERATION_RANGE = [[1, 1], [1, 1]]
            self.DPI = 96
            self.SOCIAL_DISTANCING = False

            self.SUBJECT_TYPE = SubjectTypes.SUBJECT

            self.BUTTONS_CONFIG = {}
            self.BUTTONS_CONFIG["START"] = dict(text = "Start", **Theme().button_attributes)
            self.BUTTONS_CONFIG["PAUSE"] = dict(text = "Pause", **Theme().button_attributes)
            self.BUTTONS_CONFIG["RESET"] = dict(text = "Reset", **Theme().button_attributes)

    def get_main_canvas_size_tikinter(self):
        return "{}x{}".format(self.MAIN_CANVAS_SIZE[0], self.MAIN_CANVAS_SIZE[1])

    def get_header_frame_dimensions(self):
        return [self.MAIN_CANVAS_SIZE[0], self.HEADER_FRAME_HEIGHT]

    def get_dimensions(self, column, key):
        if(column == -1):
            col_ratio = 1
        else:
            col_ratio = self.COLUMNS_RATIO if column == 0  else 1 - self.COLUMNS_RATIO
        col_width = col_ratio * self.MAIN_CANVAS_SIZE[0]
        row_ratio = getattr(self, key)
        row_height = row_ratio * self.MAIN_CANVAS_SIZE[1]
        return [int(col_width), int(row_height)]