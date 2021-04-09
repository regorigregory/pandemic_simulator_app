from enum import Enum

class Constants(Enum):
    INFECTION_RADIUS = [0.2, 0.5]
    RECOVERY_TIME = [7,30]
    INCUBATION_PERIOD = [2,10]
    INFECTION_PROBABILITY_PER_TIME_PERIOD = [0.3, 0.5]
    NUMBER_OF_SUBJECTS = 1000
    SOCIAL_DISTANCE_FACTOR = 0
    DIMENSIONS = [[0, 1024],
                  [0, 768]]
    VELOCITY_RANGE = [[-5, 5],
                  [-5, 5]]
    ACCELERATION_RANGE =  [[1,1], [1,1]]
    PARTICLE_RADIUS = 3
    DPI = 96
class Edges(Enum):
    NOT = -1
    HORIZONTAL = 0
    VERTICAL = 1