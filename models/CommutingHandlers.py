from __future__ import annotations
from models.ConfigureMe import MainConfiguration
from models.Subject import Subject
import numpy as np


class QuarantineHandler(object):

    def __init__(self):
        self.config = MainConfiguration()
        self.q_dim = self.config.get_quarantine_dimensions()

        self.quarantine_centre = np.array([self.q_dim["x"] + self.q_dim["width"] / 2,
                                  self.q_dim["y"] + self.q_dim["height"] / 2])
        self.quarantine_approaching_speed = self.config.QUARANTINE_APPROACHING_SPEED
        self.to_be_quarantined = set()
        self.in_quarantine = set()

    def head_to_quarantine(self, to_be_quarantined: Subject) -> None:
        particle = to_be_quarantined.get_particle_component()
        direction_vector = self.quarantine_centre - np.array(particle.position_vector)
        direction_vector /=  np.sum(direction_vector ** 2) ** 0.5
        particle.velocity_vector = direction_vector * self.quarantine_approaching_speed


    def handle_infected_subjects(self, infected_subjects: list[Subject], timestamp) -> set[Subject]:
        immune_and_infected = dict(INFECTED = set(), IMMUNE = set())
        for subject in infected_subjects:
            immune_and_infected[subject.get_infection_status(timestamp).name].add(subject)
            if not subject.already_in_quarantine:
                if not subject.on_my_way_to_quarantine:
                    self.head_to_quarantine(subject)
                    subject.on_my_way_to_quarantine = True

                future_location = subject.get_particle_component().position_vector + subject.get_particle_component().velocity_vector

                if (future_location[0] < self.quarantine_centre[0]):
                    subject.get_particle_component().position_vector = self.quarantine_centre
                    subject.already_in_quarantine = True
                    subject.get_particle_component().velocity_vector = np.random.uniform(*self.config.SUBJECT_VELOCITY, [2,])
                    subject.get_particle_component().set_boundaries(self.config.get_particle_quarantine_position_boundaries())

                else:
                    subject.get_particle_component().update_location_controlled()

            else:
                subject.get_particle_component().update_location()
        return immune_and_infected

class CommunityCommuteHandler:
    def __init__(self, community_boundaries):
        self.config = MainConfiguration()
        self.community_boundaries = community_boundaries
        self.rows = self.config.COMMUNITIES_ROWS
        self.columns = self.config.COMMUNITIES_COLUMNS
        self.cell_number = self.rows * self.columns

if __name__ == "__main__":
    x = 1







