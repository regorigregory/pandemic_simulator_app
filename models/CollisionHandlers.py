from __future__ import annotations
from models.Subject import Subject
from abc import ABC, abstractmethod

from models.ConfigureMe import MainConfiguration, InfectionStatuses
import numpy as np


class CollisionHandlerInterface(ABC):
    def __init__(self):
        self.config = MainConfiguration()
        self.do_i_quarantine = self.config.QUARANTINE_MODE.get()
        self.do_i_socially_distance = self.config.SOCIAL_DISTANCING_MODE.get()
        self.observers = []
        self.quarantine_split_counts = dict()

        self.last_timestamp = -1
        self.infection_distance = MainConfiguration().SUBJECT_SIZE + MainConfiguration().SUBJECT_INFECTION_RADIUS

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


class AxisBased(CollisionHandlerInterface):

    def __init__(self):
        super().__init__()

    def many_to_many(self, timestamp: int, subjects = None) -> None:
        if subjects is None:
            if(self.config.QUARANTINE_MODE.get() == False):
                subjects = self.counts["SUSCEPTIBLE"].union(self.counts["INFECTED"].union(self.counts["ASYMPTOMATIC"].union()))
                self.init_counts(exception = ["IMMUNE"])
            else:
                subjects = self.counts["SUSCEPTIBLE"].union(
                    self.counts["ASYMPTOMATIC"].union())
                self.init_counts(exception=["IMMUNE", "INFECTED"])

        x_sorted = sorted(subjects, key=lambda s: s.get_particle_component().position_x)
        for i, current in enumerate(x_sorted):
            if current.travelling is False and current.on_my_way_to_quarantine is False:
                self.one_to_many(timestamp, current, x_sorted, i)
            self.counts[current.get_infection_status(timestamp).name].add(current)



    def one_to_many(self, one: Subject, x_sorted: List[Subject], i: int, timestamp: int,) -> None:
        down = i - 1
        up = i + 1

        downward_comparator = lambda index: index >= 0
        self.handle_subjects(one, x_sorted, down, -1, downward_comparator, timestamp)

        upward_comparator = lambda index: index < len(x_sorted)
        self.handle_subjects(one, x_sorted, up, 1, upward_comparator, timestamp)

    def handle_subjects(self, one, x_sorted, index, increment, comparator_function, timestamp):

        while comparator_function(index):

            another = x_sorted[index]
            index += increment
            if (self.do_i_quarantine == True and another.get_infection_status(
                timestamp) == InfectionStatuses.INFECTED) or another.travelling:
                continue

            max_distance = one.get_behavioural_distance() + another.get_behavioural_distance()
            distance_norm, future_one, future_another = AxisBased.calculate_future_distance_between(one, another)
            one_x = future_one[0]
            another_x = future_another[0]
            x_distance = abs(one_x - another_x)
            if x_distance > max_distance:
                break

            if self.do_i_socially_distance and distance_norm < max_distance:
                one.resolve_collision(another)
            if distance_norm < self.infection_distance:
                one.encounter_with(timestamp, another)

    def count_them(self, timestamp, subjects) -> None:
        super().count_them(timestamp, subjects)

    @staticmethod
    def calculate_future_distance_between(one: Subject, another: Subject):
        p1 = one.get_particle_component().position_vector + one.get_particle_component().velocity_vector
        p2 = another.get_particle_component().position_vector + another.get_particle_component().velocity_vector
        return np.sqrt(np.sum((p2 - p1) ** 2)), p1, p2

if __name__ == "__main__":
    testObject = AxisBased()
