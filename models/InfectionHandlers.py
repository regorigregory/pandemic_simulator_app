from models.Subject import Subject
from typing import List, Set
from abc import ABC, abstractmethod
import threading
import math
from models.ConfigureMe import MainConfiguration
import numpy as np

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

    def one_to_many(self, timestamp: int, one: Subject, x_sorted: List[Subject], i: int):
        #if current.is_infected(timestamp):
        down = i - 1
        up = i + 1

        downward_comparator = lambda index: index >= 0
        self.handle_subjects(one, x_sorted, down, -1, downward_comparator, timestamp)

        upward_comparator = lambda index: index < len(x_sorted)

        self.handle_subjects(one, x_sorted, up, 1, upward_comparator, timestamp)

    def handle_subjects(self, one, x_sorted, index, increment, comparator_function, timestamp):

        infection_distance = MainConfiguration().SUBJECT_SIZE + MainConfiguration().INFECTION_RADIUS

        while comparator_function(index):
            another = x_sorted[index]
            max_distance = one.get_behavioural_distance() + another.get_behavioural_distance()
            my_x = one.get_particle_component().position_x + one.get_particle_component().velocity_x
            other_x = another.get_particle_component().position_x + another.get_particle_component().velocity_x
            x_distance = abs(my_x - other_x)

            if x_distance > max_distance:
                break
            distance_norm = self.calulate_future_distance(one, another)

            if distance_norm < max_distance:
                one.resolve_collision(another)
            if distance_norm < infection_distance:
                one.encounter_with(timestamp, another)
            index += increment

    def count_them(self, timestamp, subjects) -> None:
        super().count_them(timestamp, subjects)

    def calulate_future_distance(self, one: Subject, another: Subject):
        p1 = one.get_particle_component().position_vector + one.get_particle_component().velocity_vector
        p2 = another.get_particle_component().position_vector + another.get_particle_component().velocity_vector
        return np.sqrt(np.sum((p2 - p1) ** 2))

if __name__ == "__main__":
    testObject = AxisBased()
