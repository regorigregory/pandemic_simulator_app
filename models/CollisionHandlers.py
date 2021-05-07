from __future__ import annotations

import numpy as np
from abc import ABC, abstractmethod
from models.ConfigureMe import MainConfiguration, InfectionStatuses
from models.Subject import Subject


class AbstractCollisionHandler(ABC):
    def __init__(self):
        self.config = MainConfiguration()
        self.do_i_quarantine = self.config.QUARANTINE_MODE.get()
        self.do_i_socially_distance = self.config.SOCIAL_DISTANCING_MODE.get()
        self.infection_distance = MainConfiguration().SUBJECT_SIZE + MainConfiguration().SUBJECT_INFECTION_RADIUS

    @staticmethod
    def calculate_future_distance_between(one: Subject, another: Subject):
        p1 = one.get_particle_component().position_vector + one.get_particle_component().velocity_vector
        p2 = another.get_particle_component().position_vector + another.get_particle_component().velocity_vector
        return np.sqrt(np.sum((p2 - p1) ** 2)), p1, p2

    @abstractmethod
    def one_to_many(self, one: Subject, x_sorted: List[Subject], i: int, timestamp: int) -> None:
        pass



class AxisBased(AbstractCollisionHandler):

    def __init__(self):
        super().__init__()

    def one_to_many(self, one: Subject, x_sorted: List[Subject], i: int, timestamp: int) -> None:
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
            if (self.do_i_quarantine is True and another.get_infection_status(
                    timestamp) == InfectionStatuses.INFECTED) or another.travelling:
                continue

            max_distance = one.get_behavioural_distance() + another.get_behavioural_distance()
            distance_norm, future_one, future_another = AxisBased.calculate_future_distance_between(one, another)

            x_distance = np.abs(future_one[0] - future_another[0])

            if x_distance > max_distance:
                break
            if self.do_i_socially_distance and distance_norm < max_distance:
                one.resolve_collision(another)
            if distance_norm < self.infection_distance:
                one.encounter_with(timestamp, another)


if __name__ == "__main__":
    testObject = AxisBased()
