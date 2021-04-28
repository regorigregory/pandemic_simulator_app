from __future__ import annotations
from models.Subject import Subject
from abc import ABC, abstractmethod

from models.ConfigureMe import MainConfiguration, InfectionStatuses
import numpy as np


class InfectionHandlerInterface(ABC):
    def __init__(self):
        self.counts = dict()
        self.quarantine_split_counts = dict()
        self.init_counts()

    def init_counts(self) -> None:

        self.counts = dict(
            SUSCEPTIBLE=set(),
            ASYMPTOMATIC=set(),
            INFECTED=set(),
            IMMUNE=set()
        )
        self.quarantine_split_counts = dict(INFECTED = set(),
                                            OTHERS = set())

    def print_counts(self) -> None:
        import sys
        sys.stdout.write("\nInfected: {}, Asymptomatic: {},  Immune: {}, Susceptible: {}".format(
            len(self.counts["INFECTED"]),
            len(self.counts["ASYMPTOMATIC"]),
            len(self.counts["IMMUNE"]),
            len(self.counts["SUSCEPTIBLE"])

        ))

    def count_them(self, timestamp, subjects) -> None:

        self.init_counts()
        for subject in subjects:
            self.counts[subject.get_infection_status(timestamp).name].add(subject)


    @abstractmethod
    def many_to_many(self, timestamp, grids):
        pass

    @abstractmethod
    def one_to_many(self, timestamp: int, a_subject: Subject, subjects: list[list[Subject]]) -> None:
        pass


class AxisBased(InfectionHandlerInterface):

    def __init__(self):
        super().__init__()
        self.config = MainConfiguration()
        self.observers = []

    def many_to_many(self, timestamp: int, subjects: List[Subject]) -> None:
        self.init_counts()
        subjects = subjects[0]
        #if len(self.counts["INFECTED"]) == 0 and len(self.counts["IMMUNE"]) != 0:
        #    return

        x_sorted = sorted(subjects, key=lambda s: s.get_particle_component().position_x)
        for i, current in enumerate(x_sorted):
            self.one_to_many(timestamp, current, x_sorted, i)
            self.counts[current.get_infection_status(timestamp).name].add(current)
            if current.get_infection_status(timestamp) == InfectionStatuses.INFECTED:
                self.quarantine_split_counts["INFECTED"].add(current)
            else:
                self.quarantine_split_counts["OTHERS"].add(current)

    def one_to_many(self, timestamp: int, one: Subject, x_sorted: List[Subject], i: int) -> None:
        down = i - 1
        up = i + 1

        downward_comparator = lambda index: index >= 0
        self.handle_subjects(one, x_sorted, down, -1, downward_comparator, timestamp)

        upward_comparator = lambda index: index < len(x_sorted)

        self.handle_subjects(one, x_sorted, up, 1, upward_comparator, timestamp)

    def handle_subjects(self, one, x_sorted, index, increment, comparator_function, timestamp):
        if self.config.QUARANTINE_MODE.get() == True and one.get_infection_status(timestamp) == InfectionStatuses.INFECTED:
            return
        infection_distance = MainConfiguration().SUBJECT_SIZE + MainConfiguration().INFECTION_RADIUS

        while comparator_function(index):

            another = x_sorted[index]
            index += increment
            if self.config.QUARANTINE_MODE.get() == True and another.get_infection_status(
                timestamp) == InfectionStatuses.INFECTED:
                continue

            max_distance = one.get_behavioural_distance() + another.get_behavioural_distance()
            my_x = one.get_particle_component().position_x + one.get_particle_component().velocity_x
            other_x = another.get_particle_component().position_x + another.get_particle_component().velocity_x
            x_distance = abs(my_x - other_x)

            if x_distance > max_distance:
                break
            distance_norm = AxisBased.calulate_future_distance(one, another)

            if distance_norm < max_distance:
                one.resolve_collision(another)
            if distance_norm < infection_distance:
                one.encounter_with(timestamp, another)

    def count_them(self, timestamp, subjects) -> None:
        super().count_them(timestamp, subjects)

    @staticmethod
    def calulate_future_distance(one: Subject, another: Subject):
        p1 = one.get_particle_component().position_vector + one.get_particle_component().velocity_vector
        p2 = another.get_particle_component().position_vector + another.get_particle_component().velocity_vector
        return np.sqrt(np.sum((p2 - p1) ** 2))

if __name__ == "__main__":
    testObject = AxisBased()
