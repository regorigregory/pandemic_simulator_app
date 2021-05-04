from __future__ import annotations
from models.ConfigureMe import MainConfiguration
from models.Subject import Subject
import numpy as np
from abc import ABC, abstractmethod


class AbstractMovementHandler(ABC):

    def __init__(self):
        self.config = MainConfiguration()
        self.travelling_speed = self.config.QUARANTINE_APPROACHING_SPEED

    def set_direction_to_destination(self, to_be_guided: Subject, coordinate: list[float, float]) -> None:
        particle = to_be_guided.get_particle_component()
        direction_vector = coordinate - particle.position_vector
        direction_vector /= np.sum(direction_vector ** 2) ** 0.5
        particle.velocity_vector = direction_vector * self.travelling_speed

    @staticmethod
    def calculate_distance(point_from, point_to):
        return np.sum((point_to - point_from) ** 2) ** 0.5

    def _get_box_centre(self, box_bounds: dict[str, float]) -> np.array[float, float]:
        if isinstance(box_bounds, dict):
            return np.array([box_bounds["x"] + box_bounds["width"] / 2,
                      box_bounds["y"] + box_bounds["height"] / 2])
        else:
            width = box_bounds[0][1] - box_bounds[0][0]
            height = box_bounds[1][1] - box_bounds[1][0]

            return np.array([box_bounds[0][0] + width/2,
                             box_bounds[1][0] + height/2])

    @abstractmethod
    def handle_designated_subjects(self, designated_subjects: list[Subject], timestamp) -> set[Subject]:
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

    def handle_designated_subjects(self, designated_subjects: list[Subject], timestamp) -> set[Subject]:
        immune_and_infected = dict(INFECTED = set(), IMMUNE = set())
        for subject in designated_subjects:
            immune_and_infected[subject.get_infection_status(timestamp).name].add(subject)
            if not subject.already_in_quarantine:
                if not subject.on_my_way_to_quarantine:
                    self.set_direction_to_destination(subject)
                    subject.on_my_way_to_quarantine = True

                future_location = subject.get_particle_component().position_vector + subject.get_particle_component().velocity_vector

                if (future_location[0] < self.quarantine_centre[0]):
                    subject.get_particle_component().position_vector = self.quarantine_centre
                    subject.already_in_quarantine = True
                    subject.get_particle_component().velocity_vector = np.random.uniform(*self.config.SUBJECT_VELOCITY, [2,])
                    subject.get_particle_component().set_boundaries(self.config.get_particle_quarantine_position_boundaries())

                else:
                    subject.get_particle_component().update_location_guided()

            else:
                subject.get_particle_component().update_location()
        return immune_and_infected

    def handle_one_subject(self, subject):

        if not subject.already_in_quarantine:
            if not subject.on_my_way_to_quarantine:
                self.set_direction_to_destination(subject)
                subject.on_my_way_to_quarantine = True

            future_location = subject.get_particle_component().position_vector + subject.get_particle_component().velocity_vector

            if (future_location[0] < self.quarantine_centre[0]):
                subject.get_particle_component().position_vector = self.quarantine_centre
                subject.already_in_quarantine = True
                subject.get_particle_component().velocity_vector = np.random.uniform(*self.config.SUBJECT_VELOCITY,
                                                                                     [2, ])
                subject.get_particle_component().set_boundaries(
                    self.config.get_particle_quarantine_position_boundaries())

            else:
                subject.get_particle_component().update_location_guided()

        else:
            subject.get_particle_component().update_location()


class CommunityHandler(AbstractMovementHandler):

    def __init__(self):
        super().__init__()
        self.community_boundaries = self.config.get_community_cells_border_bounds()

        self.community_travel_chance = self.config.COMMUNITIES_VISIT_CHANCE
        self.rows = self.config.COMMUNITIES_ROWS
        self.columns = self.config.COMMUNITIES_COLUMNS
        self.cell_number = self.rows * self.columns
        self.cell_centres = [self._get_box_centre(arr) for arr in self.community_boundaries]

    def get_generator_for_loop(self, subject_in_some_dimensional_array, cell_based = True):
        def cell_based_gen():
            for cell in subject_in_some_dimensional_array:
                for subject in cell:
                    yield subject

        def non_cell_based_gen():
            for subject in subject_in_some_dimensional_array:
                yield subject

        return cell_based_gen if cell_based else non_cell_based_gen

    def handle_designated_subjects(self, designated_subjects: set[Subject], timestamp) -> set[Subject]:

        for subject in designated_subjects:
            #immune_and_infected[subject.get_infection_status(timestamp).name].add(subject)
            if not subject.travelling and not subject.on_my_way_to_quarantine:
                chance = np.random.uniform(0, 1)
                if chance < self.config.COMMUNITIES_VISIT_CHANCE:
                    subject.travelling = True
                    temp =  np.random.randint(0, self.cell_number)

                    while temp == subject.cell_id:
                        temp = np.random.randint(0, self.cell_number)
                    subject.cell_id = temp

                    self.set_direction_to_destination(subject, self.cell_centres[subject.cell_id])
                else:
                    subject.get_particle_component().update_location()

            if subject.travelling:
                destination = self.cell_centres[subject.cell_id]
                future_location = subject.get_particle_component().position_vector +\
                                  subject.get_particle_component().velocity_vector
                comparison = \
                    CommunityHandler.calculate_distance(destination, future_location) >\
                    CommunityHandler.calculate_distance(destination, subject.get_particle_component().position_vector)

                if comparison:
                    subject.get_particle_component().position_vector = destination
                    subject.get_particle_component().velocity_vector = np.random.uniform(*self.config.SUBJECT_VELOCITY,
                                                                                         [2, ])
                    subject.get_particle_component().set_boundaries(self.community_boundaries[subject.cell_id])
                    subject.travelling = False
                else:
                    subject.get_particle_component().update_location_guided()

        return dict()


if __name__ == "__main__":
    x = 1







