from models.Subject import Subject
from typing import List, Set
from abc import ABC, abstractmethod
import threading
import math
from models.ConfigureMe import MainConfiguration

class SingletonInfectionHandler(object):
    _shared_data = dict()
    instance = None

    def __new__(cls):
        if cls.instance is None:
            return super(SingletonInfectionHandler, cls).__new__(cls)
        else:
            return cls.instance

    def __init__(self):
        if SingletonInfectionHandler.instance is None:
            SingletonInfectionHandler.instance = self
            SingletonInfectionHandler.instance.__dict__ = SingletonInfectionHandler._shared_data


class InfectionHandlerInterface(ABC):
    def __init__(self):
        self._n_threads = MainConfiguration().NUMBER_OF_THREADS
        self.init_counts()

    def init_counts(self) -> dict:

        self.counts = dict(
            SUSCEPTIBLE=set(),
            INFECTED=set(),
            IMMUNE=set()
        )

    def print_counts(self) -> None:
        import sys
        sys.stdout.write("\nInfected: {}, Immune: {}, Susceptible: {}".format(
            len(self.counts["INFECTED"]),
            len(self.counts["IMMUNE"]),
            len(self.counts["SUSCEPTIBLE"])

        ))

    def count_them(self, timestamp, subjects) -> None:

        self.init_counts()
        for subject in subjects:
            self.counts[subject.get_infection_status(timestamp).name].add(subject)

    def count_them_threaded(self, timestamp, subjects) -> None:

        lock = threading.Lock()

        self.init_counts()

        def thread_helper(subjects, timestamp):
            for subject in subjects:
                lock.acquire()
                self.counts[subject.get_infection_status(timestamp).name].add(subject)
                lock.release()

        index_increment = math.ceil(len(subjects) / (self._n_threads))
        index_start = 0
        threads = []

        for thread in range(int(self._n_threads)):
            subset = subjects[index_start: int(index_start + index_increment)]
            t = threading.Thread(target=thread_helper, args=(subset, timestamp))
            t.start()
            threads.append(t)
            index_start += index_increment
        for t in threads:
            t.join()

    @abstractmethod
    def many_to_many(self, timestamp, grids):
        pass

    @abstractmethod
    def one_to_many(self, timestamp: int, a_subject: Subject, subjects: List[List[Subject]]):
        pass


class Naive(InfectionHandlerInterface):
    def __init__(self):
        super().__init__()

    def many_to_many(self, timestamp: int, grids: List[Set[Subject]]):

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
            t = threading.Thread(target=thread_function, args=(slice,))
            t.start()

    def one_to_many(self, timestamp: int, a_subject: Subject, subjects: List[List[Subject]]):
        l = threading.Lock()
        for other in subjects:
            if (a_subject == other):
                continue
            if (not other.is_immune(timestamp)):
                if (a_subject.are_we_too_close(other)
                        and a_subject.is_infected(timestamp)
                        != other.is_infected(timestamp)):
                    # l.acquire()
                    a_subject.encounter_with(timestamp, other)
                    # l.release()
            self.counts[a_subject.get_infection_status(timestamp).name].add(a_subject)


class AxisBased(InfectionHandlerInterface):

    def __init__(self):
        super().__init__()
        self.observers = []


    def many_to_many(self, timestamp: int, subjects: List[Subject]):
        subjects = subjects[0]
        if (len(self.counts["INFECTED"]) == 0 and len(self.counts["IMMUNE"]) != 0):
            return

        x_sorted = sorted(subjects, key=lambda s: s.get_particle_component().position_x)
        for i, current in enumerate(x_sorted):
            self.one_to_many(timestamp, current, x_sorted, i)
        self.init_counts()
        self.count_them(timestamp, subjects)

    def one_to_many(self, timestamp: int, current: Subject, x_sorted: List[Subject], i: int):
        if (current.is_infected(timestamp)):
            down = i - 1
            up = i + 1
            current_x = current.get_particle_component().position_x
            max_distance = current.get_infection_radius() + current.get_particle_component().get_radius()
            while (down > 0):
                other = x_sorted[down]
                other_x = other.get_particle_component().position_x
                current_distance = abs(current_x - other_x)
                if (current_distance > max_distance):
                    break
                if (other.is_infected(timestamp) or other.is_immune(timestamp)):
                    down -= 1
                    continue
                if not current.are_we_too_close(other):
                    down -= 1
                    continue
                current.encounter_with(timestamp, other)
                down -= 1

            while (up < len(x_sorted)):
                other = x_sorted[up]
                other_x = other.get_particle_component().position_x
                if (abs(current_x - other_x) > max_distance):
                    break
                if (other.is_infected(timestamp) or other.is_immune(timestamp)):
                    up += 1
                    continue
                if not current.are_we_too_close(other):
                    up += 1
                    continue
                current.encounter_with(timestamp, other)
                up += 1



    def count_them(self, timestamp, subjects) -> None:
        super().count_them(timestamp, subjects)

class ParallelAxisBased(AxisBased):

    def many_to_many(self, timestamp: int, subjects: List[Subject]):
        subjects = subjects[0]
        if (len(self.counts["INFECTED"]) == 0 and len(self.counts["IMMUNE"]) != 0):
            return

        def thread_helper(subset: List[Subject], x_sorted: List[Subject], index_start: int, timestamp: int):
            for (sub_index, current) in enumerate(subset):
                i = index_start + sub_index
                self.one_to_many(timestamp, current, x_sorted, i)

        x_sorted = sorted(subjects, key=lambda s: s.get_particle_component().position_x)

        index_increment = math.ceil(len(x_sorted) / self._n_threads)
        index_start = 0
        threads = []
        for thread in range(self._n_threads):
            subset = x_sorted[index_start: int(index_start + index_increment)].copy()
            t = threading.Thread(target=thread_helper, args=(subset, x_sorted.copy(), index_start, timestamp))
            t.start()
            threads.append(t)
            index_start += index_increment
        for t in threads:
            t.join()
        self.init_counts()


if __name__ == "__main__":
    testObject = Naive()
