from models.Subject import Subject
from typing import List, Set
from models.conf import InfectionStatuses
from abc import ABC, abstractmethod
import threading
import math

class InfectionHandlerInterface(ABC):
    def __init__(self):
        self.init_counts()

    def init_counts(self):
        self.counts = dict(
            SUSCEPTIBLE=set(),
            INFECTED=set(),
            IMMUNE=set()
        )
    def print_counts(self):
        import sys
        sys.stdout.write("\nInfected: {}, Immune: {}, Susceptible: {}".format(
            len(self.counts["INFECTED"]),
            len(self.counts["IMMUNE"]),
            len(self.counts["SUSCEPTIBLE"])

        ))

    def count_them(self, timestamp, subjects):
        for subject in subjects:
            self.counts[subject.get_infection_status(timestamp).name].add(subject)

class Naive(InfectionHandlerInterface):
    def __init__(self):
        super().__init__()
        self._n_threads = 8


    def many_to_many(self, timestamp:int, grids: List[Set[Subject]]):
        self.init_counts()

        def thread_function(grids: List[Set[Subject]]):
            for subjects in grids:
                for a_subject in subjects:
                    if (a_subject.is_immune(timestamp)):
                        self.counts["IMMUNE"].add(a_subject)
                    else:
                        self.one_to_many(timestamp, a_subject, subjects)

        flat_grid = grids.flatten()
        grid_increment = math.ceil(flat_grid.shape[0] / self._n_threads)
        grid_start = 0
        for thread in range(self._n_threads):
            slice = flat_grid[grid_start: int(grid_start + grid_increment)]
            grid_start += grid_increment
            t = threading.Thread(target = thread_function, args=(slice,))
            t.start()

    def one_to_many(self, timestamp: int, a_subject: Subject, subjects: List[Subject]):

            for other in subjects:
                if (a_subject == other):
                    continue
                if(not other.is_immune(timestamp)):
                    if (a_subject.are_we_too_close(other)
                            and a_subject.is_infected(timestamp)
                            != other.is_infected(timestamp)):

                        a_subject.encounter_with(timestamp, other)
                self.counts[a_subject.get_infection_status(timestamp).name].add(a_subject)


class AxisBased(InfectionHandlerInterface):
    def __init__(self, config):
        super().__init__(config)
        self._gridsize = (config.INFECTION_RADIUS.value + config.PARTICLE_RADIUS.value) \
                         * 2 * config.SUBJECTS_PER_GRID.value

    def many_to_many(self, timestamp: int, subjects: List[Subject]):
        self.init_counts()
        subjects.sort(key = lambda s: s.get_particle_component().position_x)

        for a_subject in subjects:
            if (a_subject.is_immune(timestamp)):
                self.counts["IMMUNE"].add(a_subject)
            else:
                self.one_to_many(timestamp, a_subject, subjects)

    def one_to_many(self, timestamp: int, a_subject: Subject, subjects: List[Subject]):

            for other in subjects:
                if (a_subject == other):
                    continue
                if(not other.is_immune(timestamp)):
                    if (a_subject.are_we_too_close(other)
                            and a_subject.is_infected(timestamp)
                            != other.is_infected(timestamp)):

                        a_subject.encounter_with(timestamp, other)
                self.counts[a_subject.get_infection_status(timestamp).name].add(a_subject)

if __name__ == "__main__":
    testObject = Naive()