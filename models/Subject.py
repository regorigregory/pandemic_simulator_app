import math
from models.conf import InfectionStatuses, Constants
from models.Particle import Particle
from enum import Enum
import numpy as np

class Subject:

    def __init__(self, config: Enum, am_i_infected = False):

        self._infection_radius = Subject.set_random_attribute_safely(config.INFECTION_RADIUS.value)
        self._recovery_time = Subject.set_random_attribute_safely(config.INFECTION_RADIUS.value)
        self._incubation_period = Subject.set_random_attribute_safely(config.INCUBATION_PERIOD.value)
        self._infection_probability = Subject.set_random_attribute_safely(config.INFECTION_PROBABILITY_PER_TIME_PERIOD.value)

        self._particle = Particle(config)
        self._infection_radius = self._particle.get_radius() + config.INFECTION_RADIUS.value
        if np.random.uniform() <= self.get_infection_probability():
            self._infection_status = InfectionStatuses.INFECTED
            self._got_infected_at = 0
        else:
            self._infection_status = InfectionStatuses.SUSCEPTIBLE
            self._got_infected_at = -1


    def get_infection_radius(self):
        return self._infection_radius

    def get_particle_component(self):
        return self._particle

    def _have_i_recovered(self, timestamp: int) -> bool:
        if timestamp - self._got_infected_at >= self._recovery_time:
            return True
        return False

    def get_infection_timestamp(self):
        return self._got_infected_at

    def get_infection_status(self, timestamp: int) -> InfectionStatuses:
        if(self._infection_status == InfectionStatuses.INFECTED
                and self._have_i_recovered(timestamp)):
            self._infection_status = InfectionStatuses.IMMUNE
        return self._infection_status

    def infect_me_if_you_can(self, timestamp, other):
        if (self.get_infection_status(timestamp) == InfectionStatuses.SUSCEPTIBLE
                and other.get_infection_status(timestamp) == InfectionStatuses.INFECTED
            #and self.get_infection_probability() >= random.random()
            ):
            self.infect_me(timestamp)

    def get_infection_probability(self) -> float:
        return self._infection_probability

    def get_recovery_time(self) -> float:
        return self._recovery_time

    def infect_me(self, timestamp):
        if self.get_infection_status(timestamp) == InfectionStatuses.SUSCEPTIBLE:
            self._infection_status = InfectionStatuses.INFECTED
            self._got_infected_at = timestamp

    def encounter_with(self, timestamp, other) -> None:
        self.infect_me_if_you_can(timestamp, other)
        other.infect_me_if_you_can(timestamp, self)

    def are_we_too_close(self, other):
        p1 = self.get_particle_component().position_vector
        p2 = other.get_particle_component().position_vector
        distance = np.sqrt(np.sum((p2 - p1)**2))
        if self.get_infection_radius() >= distance:
            return True
        return False

    @staticmethod
    def set_random_attribute_safely(const_or_arr):
        if isinstance(const_or_arr, list):
            return np.random.uniform(*const_or_arr)
        return const_or_arr


if __name__ == "__main__":
    testA = Subject(Constants)
    testB = Subject(Constants)


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
    testC = Subject(Constants)