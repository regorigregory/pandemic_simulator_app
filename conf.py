from enum import Enum

class Constants(Enum):
    INFECTION_RADIOUS = [0.2, 0.5]
    RECOVERY_TIME = [7,30]
    INCUBATION_PERIOD = [2,10]
    INFECTION_PROBABILITY_PER_TIME_PERIOD = [0.3, 0.5]
    NUMBER_OF_SUBJECTS = 10
    SOCIAL_DISTANCE_FACTOR = 0
    DIMENSIONS = [[0, 1024],
                  [0, 768]]
    VELOCITY_RANGE = [[0, 1],
                  [0, 1]]
    ACCELERATION_RANGE =  [[0, 1],
                  [0, 1]]
class Edges(Enum):
    NOT = -1
    HORIZONTAL = 0
    VERTICAL = 1