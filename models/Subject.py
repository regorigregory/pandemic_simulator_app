from __future__ import annotations
from models.ConfigureMe import InfectionStatuses, MainConfiguration
from models.Particle import Particle
import numpy as np
from models.ConfigureMe import MainConfiguration
from typing import List, Union

class Subject:

    def __init__(self, config = MainConfiguration(), am_i_infected = False):
        self.on_my_way_to_quarantine = False
        self.already_in_quarantine = False
        self.quarantine_mode = False
        self._infection_radius = Subject.set_random_attribute_safely(config.INFECTION_RADIUS)

        self._recovery_time = config.RECOVERY_TIME * config.FRAME_MULTIPLIER
        self._incubation_period = config.INCUBATION_PERIOD * config.FRAME_MULTIPLIER

        self._infection_probability = Subject.set_random_attribute_safely(config.CHANCE_OF_INFECTION/config.FRAME_MULTIPLIER)
        self._do_i_socially_distance = MainConfiguration().SUBJECT_COMPLIANCE > np.random.uniform(0, 1) \
            if MainConfiguration().SOCIAL_DISTANCING_MODE.get() else False

        self._particle = Particle(config)
        self._infection_radius = self._particle.get_radius() + config.INFECTION_RADIUS

        if np.random.uniform() <= config.INITIAL_INFECTION_RATIO:
            self._infection_status = InfectionStatuses.ASYMPTOMATIC
            self._got_infected_at = 0
        else:
            self._infection_status = InfectionStatuses.SUSCEPTIBLE
            self._got_infected_at = -1
        self._last_checkup = 0

    def get_particle_component(self) -> Particle:
        return self._particle

    def _have_i_recovered(self, timestamp: int) -> bool:
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
                    + self._incubation_period< timestamp):
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

    def _infect_me_if_you_can(self, timestamp, other) -> None:
        my_status = self.get_infection_status(timestamp)
        other_status =  other.get_infection_status(timestamp)
        if (my_status == InfectionStatuses.SUSCEPTIBLE
                and (other_status == InfectionStatuses.ASYMPTOMATIC
                or  other_status == InfectionStatuses.INFECTED)
                and self.get_infection_probability() >= np.random.uniform()
                ):
            self._infect_me(timestamp)

    def _infect_me(self, timestamp) -> None:
        if self.get_infection_status(timestamp) == InfectionStatuses.SUSCEPTIBLE:
            self._infection_status = InfectionStatuses.ASYMPTOMATIC
            self._got_infected_at = timestamp

    def encounter_with(self, timestamp, other) -> None:
        self._infect_me_if_you_can(timestamp, other)
        other._infect_me_if_you_can(timestamp, self)

    def get_behavioural_distance(self):
        if self.am_i_compliant():
            return MainConfiguration().INFECTION_RADIUS - 1
        return self.get_particle_component().get_radius()

    def are_we_too_close(self, other) -> bool:

        p1 = self.get_particle_component().position_vector
        p2 = other.get_particle_component().position_vector
        distance1 = self.get_behavioural_distance()
        distance2 = other.get_behavioural_distance()
        distance = np.sqrt(np.sum((p2 - p1)**2))

        if distance1 + distance2 >= distance:
            return True
        return False

    def resolve_collision(self, other: Subject):
        if not (self.quarantine_mode == True and (self._infection_status == InfectionStatuses.INFECTED
        or other._infection_status == InfectionStatuses.INFECTED
        )):
            self.get_particle_component().resolve_collision(other.get_particle_component())

    @staticmethod
    def set_random_attribute_safely(const_or_arr) -> Union[int, List, float]:
        if isinstance(const_or_arr, list):
            return np.random.uniform(*const_or_arr)
        return const_or_arr


if __name__ == "__main__":
    testA = Subject(MainConfiguration)
    testB = Subject(MainConfiguration)


    infection_time = 1
    if(testA.get_infection_status(0) == InfectionStatuses.SUSCEPTIBLE):
        testA.infect_me(infection_time)
    print("testA is {}.".format(testA.get_infection_status(infection_time).name))
    print("testA is {}".format(testA.get_infection_status(testA.get_infection_timestamp() + testA.get_recovery_time())))
    testA.infect_me(100)
    print("testA is {} after reinfection attempt.".format(testA.get_infection_status(testA.get_infection_timestamp() + testA.get_recovery_time())))
    testA._got_infected_at = -1
    testA._infection_status = InfectionStatuses.SUSCEPTIBLE
    testB.infect_me(0)
    print("testA is {}.".format(testA.get_infection_status(infection_time).name))
    print("testB is {}.".format(testB.get_infection_status(infection_time).name))
    testA.encounter_with(infection_time, testB)
    print("After testA and testB encounters with each other:")
    print("testA is {}.".format(testA.get_infection_status(infection_time).name))
    print("testB is {}.".format(testB.get_infection_status(infection_time).name))
    testC = Subject(MainConfiguration)