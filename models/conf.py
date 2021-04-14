from enum import Enum

class InfectionStatuses(Enum):
    SUSCEPTIBLE = 0
    INFECTED = 1
    IMMUNE = 2

class SubjectTypes(Enum):
    PARTICLE = 0,
    SUBJECT = 1

class Constants(Enum):
    NUMBER_OF_CORES = 8
    NUMBER_OF_SUBJECTS = 50
    SUBJECTS_PER_GRID = 10

    INITIAL_INFECTED_SUBJECTS_RATIO = 0.2
    INFECTION_RADIUS = 40
    PARTICLE_RADIUS = 10

    RECOVERY_TIME = [50,100]
    INCUBATION_PERIOD = [2,10]

    INFECTION_PROBABILITY_PER_TIME_PERIOD = [0.5, 0.7]

    SOCIAL_DISTANCE_FACTOR = 0

    DIMENSIONS = [[0, 1024],
                  [0, 768]]

    VELOCITY_RANGE = [[-10, 10],
                  [-10, 10]]
    ACCELERATION_RANGE =  [[1,1], [1,1]]
    DPI = 96
    SOCIAL_DISTANCING = False

    SUBJECT_TYPE = SubjectTypes.SUBJECT

