from models.Subject import Subject
from typing import List, Set
from abc import ABC, abstractmethod
import threading
import math
from models.ConfigureMe import MainConfiguration


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


class AxisBased(InfectionHandlerInterface):

    def __init__(self):
        super().__init__()
        self.observers = []

    def many_to_many(self, timestamp: int, subjects: List[Subject]):
        subjects = subjects[0]
        #if len(self.counts["INFECTED"]) == 0 and len(self.counts["IMMUNE"]) != 0:
        #    return

        x_sorted = sorted(subjects, key=lambda s: s.get_particle_component().position_x)
        for i, current in enumerate(x_sorted):
            self.one_to_many(timestamp, current, x_sorted, i)
        self.init_counts()
        self.count_them(timestamp, subjects)

    def one_to_many(self, timestamp: int, current: Subject, x_sorted: List[Subject], i: int):
        #if current.is_infected(timestamp):
        down = i - 1
        up = i + 1
        current_x = current.get_particle_component().position_x
        max_distance = current.get_infection_radius() + current.get_particle_component().get_radius()

        while down > 0:
            other = x_sorted[down]
            other_x = other.get_particle_component().position_x
            current_distance = abs(current_x - other_x)

            if current_distance > max_distance:
                break

            if not current.are_we_too_close(other):
                down -= 1
                continue
            else:
                current.resolve_collision(other)
                if other.is_infected(timestamp) or other.is_immune(timestamp):
                    down -= 1
                    continue
                current.encounter_with(timestamp, other)
                down -= 1

        while up < len(x_sorted):
            other = x_sorted[up]
            other_x = other.get_particle_component().position_x
            current_distance = abs(current_x - other_x)

            if current_distance > max_distance:
                break

            if not current.are_we_too_close(other):
                up += 1
                continue
            else:
                current.resolve_collision(other)
                if other.is_infected(timestamp) or other.is_immune(timestamp):
                    up += 1
                    continue
                current.encounter_with(timestamp, other)
                up += 1

    def count_them(self, timestamp, subjects) -> None:
        super().count_them(timestamp, subjects)


if __name__ == "__main__":
    testObject = AxisBased()
