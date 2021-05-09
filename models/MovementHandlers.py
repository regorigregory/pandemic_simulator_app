from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np

from models.ConfigureMe import MainConfiguration
from models.Subject import Subject
from models.AbstractClasses import AbstractMovementHandler


class QuarantineHandler(AbstractMovementHandler):

    def __init__(self):
        super().__init__()
        self.q_dim = MainConfiguration().get_quarantine_dimensions()
        self.quarantine_centre = self._get_box_centre(self.q_dim)

        self.to_be_quarantined = set()
        self.in_quarantine = set()

    def set_direction_to_destination(self, to_be_guided: Subject) -> None:
        super().set_direction_to_destination(to_be_guided, self.quarantine_centre)

    def guide_subject_journey(self, to_be_guided: Subject) -> None:

        if not to_be_guided.already_in_quarantine:
            if not to_be_guided.on_my_way_to_quarantine:
                self.set_direction_to_destination(to_be_guided)
                to_be_guided.on_my_way_to_quarantine = True

            future_location = to_be_guided.get_particle_component().position_vector + to_be_guided.get_particle_component().velocity_vector

            if (future_location[0] < self.quarantine_centre[0]):
                to_be_guided.get_particle_component().position_vector = self.quarantine_centre
                to_be_guided.already_in_quarantine = True
                to_be_guided.get_particle_component().velocity_vector = np.random.uniform(*MainConfiguration().SUBJECT_VELOCITY,
                                                                                          [2, ])
                to_be_guided.get_particle_component().set_boundaries(
                    MainConfiguration().get_particle_quarantine_position_boundaries())


class CommunityHandler(AbstractMovementHandler):

    def __init__(self):
        super().__init__()
        self.community_boundaries = MainConfiguration().get_community_cells_border_bounds()

        self.community_travel_chance = MainConfiguration().COMMUNITIES_VISIT_CHANCE
        self.rows = MainConfiguration().COMMUNITIES_ROWS
        self.columns = MainConfiguration().COMMUNITIES_COLUMNS
        self.cell_number = self.rows * self.columns
        self.cell_centres = [self._get_box_centre(arr) for arr in self.community_boundaries]

    def set_direction_to_destination(self, subject: Subject) -> None:
        subject.travelling = True
        temp = np.random.randint(0, self.cell_number)

        while temp == subject.cell_id:
            temp = np.random.randint(0, self.cell_number)
        subject.cell_id = temp
        super().set_direction_to_destination(subject, self.cell_centres[subject.cell_id])

    def guide_subject_journey(self, to_be_guided: Subject, timestamp) -> None:
        destination = self.cell_centres[to_be_guided.cell_id]
        future_location = to_be_guided.get_particle_component().position_vector + \
                          to_be_guided.get_particle_component().velocity_vector
        comparison = \
            CommunityHandler.calculate_distance(destination, future_location) > \
            CommunityHandler.calculate_distance(destination, to_be_guided.get_particle_component().position_vector)

        if comparison:
            to_be_guided.get_particle_component().position_vector = destination
            to_be_guided.get_particle_component().velocity_vector = np.random.uniform(*MainConfiguration().SUBJECT_VELOCITY,
                                                                                      [2, ])
            to_be_guided.get_particle_component().set_boundaries(self.community_boundaries[to_be_guided.cell_id])
            to_be_guided.travelling = False
        else:
            to_be_guided.get_particle_component().update_location_guided(timestamp)

if __name__ == "__main__":
    x = 1
