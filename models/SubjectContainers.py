from models.ConfigureMe import SubjectTypes, MainConfiguration
from models.Particle import Particle
from models.Subject import Subject
from models.InfectionHandlers import InfectionHandlerInterface, AxisBased, ParallelAxisBased
import math
import numpy as np
import threading
from typing import List
import time
from abc import ABC, abstractmethod
class ContainerOfSubjects(ABC):
    @abstractmethod
    def reset(self):
        pass
    @abstractmethod
    def populate_subjects(self, config, number_of_subjects):
        pass
    @abstractmethod
    def move_guys(self, timestamp, parallel = False, infection_handling = True):
        pass

class BoxOfSubjects(ContainerOfSubjects):
    def __init__(self, config = MainConfiguration(), infection_handler = AxisBased(), number_of_subjects = None):
        self.config = config
        self.contents = []

        self._particle_radius= config.SUBJECT_SIZE
        self._infection_handler = infection_handler
        self._infection_radius = config.INFECTION_RADIUS + config.SUBJECT_SIZE
        self.populate_subjects(config, number_of_subjects)

    def reset(self):
        self = BoxOfSubjects()

    def populate_subjects(self, config, number_of_subjects):
        if config.SUBJECT_TYPE == SubjectTypes.PARTICLE:
            constructor = Particle
        else:
            constructor = Subject
        limit = number_of_subjects if number_of_subjects else config.SUBJECT_NUMBER
        for i in range(0, limit):
            p = constructor(config)
            self.contents.append(p)
            #self.add_particle_to_grids(p)

    def move_guys(self, timestamp, parallel = False, infection_handling = True):
        for particle in self.contents:
            particle.get_particle_component().update_location()
        if infection_handling:
            self._infection_handler.many_to_many(timestamp, [self.contents])


if __name__ == "__main__":

    NUMBER_OF_TESTS = 1
    NUMBER_OF_SUBJECTS = range(100, 1000, 100)
    sequential = dict()
    parallel = dict()
    print('Evaluating Sequential Implementation...')

    for num_subjects in NUMBER_OF_SUBJECTS:
        box = BoxOfSubjects(MainConfiguration, number_of_subjects=num_subjects)
        if(num_subjects not in list(sequential.keys())):
            sequential[num_subjects] = 0.0000001
        for i in range(NUMBER_OF_TESTS):
            start = time.perf_counter_ns()
            box.move_guys(i)
            end = time.perf_counter_ns()- start
            sequential[num_subjects] += end
        sequential[num_subjects] /= NUMBER_OF_TESTS

    print('Evaluating Thread based Implementation...')

    for num_subjects in NUMBER_OF_SUBJECTS:
        box = BoxOfSubjects(MainConfiguration, number_of_subjects=num_subjects)
        if(num_subjects not in list(parallel.keys())):
            parallel[num_subjects] = 0.0000001
        for i in range(NUMBER_OF_TESTS):
            start = time.perf_counter()
            box.move_guys(i, parallel = True)
            end = time.perf_counter_ns() - start
            parallel[num_subjects] += end
        parallel[num_subjects] /= NUMBER_OF_TESTS

    for a,b in zip(sequential.items(), parallel.items()):
        print('Average Sequential Time for {} particles: {:.2f} ns'.format(a[0], a[1] * 1000*1000))
        print('Average Parallell Time for {} particles: {:.2f} ns'.format(b[0], b[1] * 1000*1000))
        print('Speedup: {:.2f} ns'.format(a[1] / b[1]))
        #print('Efficiency: {:.2f}%'.format(100 * (v1 / v2) / mp.cpu_count()))