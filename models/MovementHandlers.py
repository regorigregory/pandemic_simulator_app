from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np

from models.ConfigureMe import MainConfiguration
from models.Subject import Subject


class AbstractMovementHandler(ABC):

    def __init__(self):
        self.config = MainConfiguration()
        self.travelling_speed = self.config.QUARANTINE_APPROACHING_SPEED

    def set_direction_to_destination(self, to_be_guided: Subject, coordinate: list[float, float]) -> None:
        particle = to_be_guided.get_particle_component()
        direction_vector = coordinate - particle.position_vector
        direction_vector /= np.sum(direction_vector ** 2) ** 0.5
        particle.velocity_vector = direction_vector * self.travelling_speed

    def _get_box_centre(self, box_bounds: dict[str, float]) -> np.array[float, float]:
        if isinstance(box_bounds, dict):
            return np.array([box_bounds["x"] + box_bounds["width"] / 2,
                      box_bounds["y"] + box_bounds["height"] / 2])
        else:
            width = box_bounds[0][1] - box_bounds[0][0]
            height = box_bounds[1][1] - box_bounds[1][0]

            return np.array([box_bounds[0][0] + width/2,
                             box_bounds[1][0] + height/2])

    @staticmethod
    def calculate_distance(point_from, point_to) -> float:
        return np.sum((point_to - point_from) ** 2) ** 0.5

    @abstractmethod
    def guide_subject_journey(self, to_be_guided: Subject) -> None:
        pass


class QuarantineHandler(AbstractMovementHandler):

    def __init__(self):
        super().__init__()
        self.q_dim = self.config.get_quarantine_dimensions()
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
                to_be_guided.get_particle_component().velocity_vector = np.random.uniform(*self.config.SUBJECT_VELOCITY,
                                                                                          [2, ])
                to_be_guided.get_particle_component().set_boundaries(
                    self.config.get_particle_quarantine_position_boundaries())


class CommunityHandler(AbstractMovementHandler):

    def __init__(self):
        super().__init__()
        self.community_boundaries = self.config.get_community_cells_border_bounds()

        self.community_travel_chance = self.config.COMMUNITIES_VISIT_CHANCE
        self.rows = self.config.COMMUNITIES_ROWS
        self.columns = self.config.COMMUNITIES_COLUMNS
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
            to_be_guided.get_particle_component().velocity_vector = np.random.uniform(*self.config.SUBJECT_VELOCITY,
                                                                                      [2, ])
            to_be_guided.get_particle_component().set_boundaries(self.community_boundaries[to_be_guided.cell_id])
            to_be_guided.travelling = False
        else:
            to_be_guided.get_particle_component().update_location_guided(timestamp)

if __name__ == "__main__":
    x = 1
