from __future__ import annotations

from typing import List, Union

import numpy as np

from models.ConfigureMe import InfectionStatuses
from models.ConfigureMe import MainConfiguration
from models.Particle import Particle


class Subject:
    _subject_counter = 0

    def __init__(self, boundaries=None, position=None):
        Subject._subject_counter += 1

        self.id = Subject._subject_counter
        self.n_infected = 0
        self.config = MainConfiguration()
        self.on_my_way_to_quarantine = False
        self.already_in_quarantine = False
        self.quarantine_mode = False
        self.travelling = False
        self.cell_id = -1
        self.total_sickness_time = self.config.SUBJECT_INCUBATION_PERIOD + self.config.SUBJECT_RECOVERY_TIME
        self._infection_radius = Subject.set_random_attribute_safely(self.config.SUBJECT_INFECTION_RADIUS)
        self.frames_per_day = self.config.get_frames_per_day()
        self._recovery_time = self.config.SUBJECT_RECOVERY_TIME * self.frames_per_day
        self._incubation_period = self.config.SUBJECT_INCUBATION_PERIOD * self.frames_per_day

        self._infection_probability = Subject.set_random_attribute_safely(
            self.config.SUBJECT_CHANCE_OF_INFECTION / self.frames_per_day)
        self._do_i_socially_distance = MainConfiguration().SUBJECT_COMPLIANCE > np.random.uniform(0, 1) \
            if MainConfiguration().SOCIAL_DISTANCING_MODE else False

        self._particle = Particle(boundaries=boundaries, position=position)
        self._infection_radius = self._particle.get_radius() + self.config.SUBJECT_INFECTION_RADIUS

        if np.random.uniform() <= self.config.SUBJECT_INITIAL_INFECTION_RATIO:
            self._infection_status = InfectionStatuses.ASYMPTOMATIC
            self._got_infected_at = 0
        else:
            self._infection_status = InfectionStatuses.SUSCEPTIBLE
            self._got_infected_at = -1
        self._last_checkup = 0

    def get_particle_component(self) -> Particle:
        return self._particle

    def _have_i_recovered(self) -> bool:
        return self._infection_status == InfectionStatuses.IMMUNE

    def am_i_compliant(self) -> bool:
        return self._do_i_socially_distance

    def get_infection_timestamp(self) -> int:
        return self._got_infected_at

    def get_infection_status(self, timestamp: int) -> InfectionStatuses:
        if self._last_checkup != timestamp:
            if ((self._infection_status == InfectionStatuses.INFECTED
                 or self._infection_status == InfectionStatuses.ASYMPTOMATIC)
                    and self.get_infection_timestamp()
                    + self._recovery_time
                    + self._incubation_period < timestamp):
                self._infection_status = InfectionStatuses.IMMUNE
            elif self._infection_status == InfectionStatuses.ASYMPTOMATIC and \
                    self.get_infection_timestamp() \
                    + self._incubation_period < timestamp:
                self._infection_status = InfectionStatuses.INFECTED
            self._last_checkup = timestamp
        return self._infection_status

    def is_immune(self, timestamp) -> bool:
        return self.get_infection_status(timestamp) == InfectionStatuses.IMMUNE

    def is_infected(self, timestamp) -> bool:
        return \
            self.get_infection_status(timestamp) == InfectionStatuses.INFECTED \
            or self.get_infection_status(timestamp) == InfectionStatuses.ASYMPTOMATIC

    def is_susceptible(self, timestamp) -> bool:
        return self.get_infection_status(timestamp) == InfectionStatuses.SUSCEPTIBLE

    def get_infection_probability(self) -> float:
        return self._infection_probability

    def get_recovery_time(self) -> float:
        return self._recovery_time

    def infect_me_if_you_can(self, timestamp, other) -> None:
        my_status = self.get_infection_status(timestamp)
        other_status = other.get_infection_status(timestamp)
        if (my_status == InfectionStatuses.SUSCEPTIBLE
                and (other_status == InfectionStatuses.ASYMPTOMATIC
                     or other_status == InfectionStatuses.INFECTED)
                and self.get_infection_probability() >= np.random.uniform()):
            self._infect_me(timestamp)
            return True
        return False

    def _infect_me(self, timestamp) -> None:
        if self.get_infection_status(timestamp) == InfectionStatuses.SUSCEPTIBLE:
            self._infection_status = InfectionStatuses.ASYMPTOMATIC
            self._got_infected_at = timestamp

    def increment_infected_count(self):
        self.n_infected += 1

    def estimate_total_infections(self, timestamp: int) -> float:
        current_status = self.get_infection_status(timestamp)
        if current_status == InfectionStatuses.SUSCEPTIBLE or current_status == InfectionStatuses.IMMUNE:
            return 0
        span = (timestamp - self._got_infected_at)
        if span == 0:
            span = 1
        return self.total_sickness_time * self.config.get_frames_per_day() * self.n_infected / span

    def encounter_with(self, timestamp, other: Subject) -> None:
        if self.infect_me_if_you_can(timestamp, other):
            other.increment_infected_count()
        if other.infect_me_if_you_can(timestamp, self):
            self.increment_infected_count()

    def get_behavioural_distance(self):
        if self.am_i_compliant():
            return MainConfiguration().SUBJECT_INFECTION_RADIUS + self.get_particle_component().get_radius() / 2
        return self.get_particle_component().get_radius()

    def are_we_too_close(self, other) -> bool:

        p1 = self.get_particle_component().position_vector
        p2 = other.get_particle_component().position_vector
        distance1 = self.get_behavioural_distance()
        distance2 = other.get_behavioural_distance()
        distance = np.sqrt(np.sum((p2 - p1) ** 2))

        if distance1 + distance2 >= distance:
            return True
        return False

    def resolve_collision(self, other: Subject):
            self.get_particle_component().resolve_collision(other.get_particle_component())

    @staticmethod
    def set_random_attribute_safely(const_or_arr) -> Union[int, List, float]:
        if isinstance(const_or_arr, list):
            return np.random.uniform(*const_or_arr)
        return const_or_arr

    def __key(self):
        return self.id

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Subject):
            return self.__key() == other.__key()
        return NotImplemented


if __name__ == "__main__":
    pass
