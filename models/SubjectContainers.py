from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np

from models.CollisionHandlers import AxisBased
from models.ConfigureMe import InfectionStatuses, MainConfiguration
from models.MovementHandlers import QuarantineHandler, CommunityHandler
from models.Subject import Subject


class AbstractContainerOfSubjects(ABC):
    def __init__(self):
        self.config = MainConfiguration()
        self._infection_handler = AxisBased()
        self.contents = set()
        self._particle_radius = self.config.SUBJECT_SIZE
        self._infection_radius = self.config.SUBJECT_INFECTION_RADIUS + self.config.SUBJECT_SIZE
        self.counts = dict()
        self.count_keys = ["SUSCEPTIBLE", "ASYMPTOMATIC", "INFECTED", "IMMUNE"]
        self.init_counts()

    @abstractmethod
    def reset(self) -> None:
        pass

    @abstractmethod
    def populate_subjects(self) -> None:
        pass

    @abstractmethod
    def move_guys(self, timestamp: int) -> None:
        pass

    def init_counts(self, exception=None) -> None:
        for k in self.count_keys:
            if exception is None or k not in exception:
                self.counts[k] = set()


class DefaultContainer(AbstractContainerOfSubjects):
    def __init__(self):
        super().__init__()
        self.subjects_in_cells = []
        self.rows = 3
        self.columns = 3
        self.cell_count = self.rows * self.columns
        self.init_cells()

        self.populate_subjects()
        self.do_i_quarantine = self.config.QUARANTINE_MODE.get()
        if self.do_i_quarantine:
            self._quarantine_handler = QuarantineHandler()

    def init_cells(self):
        self.subjects_in_cells = []
        for i in range(self.rows):
            self.subjects_in_cells.append([])
            for j in range(self.columns):
                self.subjects_in_cells[i].append(set())

    def reset(self):
        self = DefaultContainer()

    def populate_subjects(self):
        constructor = Subject
        limit = self.config.SUBJECT_NUMBER
        for i in range(0, limit):
            j = 0
            s = constructor(self.config)
            while j < len(self.contents):
                already_there = list(self.contents)[j]
                if s.are_we_too_close(already_there):
                    s = constructor(self.config)
                    j = 0
                else:
                    j += 1
            self.contents.add(s)

            self.add_subject_to_cell(s, self.subjects_in_cells)


    def add_subject_to_cell(self, s: Subject, cells: list[set[Subject]] = None):
        subject_radius = self.config.SUBJECT_SIZE + self.config.SUBJECT_INFECTION_RADIUS
        left = int((s.get_particle_component().position_vector[0] - subject_radius)
                   / (self.config.MAIN_CANVAS_SIZE[0] / self.columns))
        right = int((s.get_particle_component().position_vector[0] + subject_radius)
                    / (self.config.MAIN_CANVAS_SIZE[0] / self.columns))
        bottom = int((s.get_particle_component().position_vector[1] - subject_radius)
                     / (self.config.MAIN_CANVAS_SIZE[1] / self.rows))
        top = int((s.get_particle_component().position_vector[1] + subject_radius) / (
                self.config.MAIN_CANVAS_SIZE[1] / self.rows))

        cells[left][top].add(s)
        cells[right][top].add(s)
        cells[left][top].add(s)
        cells[right][bottom].add(s)


    def move_guys(self, timestamp):

        self.init_counts()
        new_cells = [[set(), set()], [set(), set()]]
        for row in self.subjects_in_cells:
            for column in row:
                x_sorted = sorted(column, key=lambda s: s.get_particle_component().position_x)
                for i, subject in enumerate(x_sorted):
                    if subject.already_in_quarantine:
                        subject.get_particle_component().update_location(timestamp)
                    elif self.do_i_quarantine and (subject.get_infection_status(
                            timestamp) == InfectionStatuses.INFECTED or subject.on_my_way_to_quarantine):
                        self._quarantine_handler.guide_subject_journey(subject)
                        subject.get_particle_component().update_location_guided(timestamp)
                    else:
                        self._infection_handler.one_to_many(subject, x_sorted, i, timestamp)
                        subject.get_particle_component().update_location(timestamp)

                    self.add_subject_to_cell(subject, new_cells)

                    self.counts[subject.get_infection_status(timestamp).name].add(subject)

        self.subjects_in_cells = new_cells


class CommunitiesContainer(AbstractContainerOfSubjects):
    def __init__(self):
        super().__init__()
        self.cell_count = self.config.COMMUNITIES_COLUMNS * self.config.COMMUNITIES_ROWS
        self.cell_coordinates = self.config.get_community_cells_border_bounds()
        self.subjects_in_cells = [set() for _ in range(self.cell_count)]
        self.populate_subjects()
        self._community_handler = CommunityHandler()

        self.do_i_quarantine = self.config.QUARANTINE_MODE.get()
        if self.do_i_quarantine:
            self._quarantine_handler = QuarantineHandler()

    def reset(self):
        self = CommunitiesContainer()

    def populate_subjects(self):
        limit = int(self.config.SUBJECT_NUMBER / self.cell_count)
        remainder = self.config.SUBJECT_NUMBER - self.cell_count * limit

        for c in range(self.cell_count):
            self.populate_cell(c, limit)
        self.populate_cell(c, remainder)

    def populate_cell(self, c, limit):
        constructor = Subject
        for i in range(limit):
            j = 0
            current_cell = self.subjects_in_cells[c]
            movement_boundaries = np.array(self.cell_coordinates[c])
            movement_boundaries[:, 0] += self.config.SUBJECT_SIZE
            movement_boundaries[:, 1] -= self.config.SUBJECT_SIZE
            s = constructor(self.config, boundaries=movement_boundaries)
            while j < len(current_cell):
                already_there = list(current_cell)[j]
                if s.are_we_too_close(already_there):
                    s = constructor(self.config, boundaries=movement_boundaries)
                    j = 0
                else:
                    j += 1
            s.cell_id = c
            current_cell.add(s)
            self.contents.add(s)

    def move_guys(self, timestamp):

        self.init_counts()
        new_cells = [set() for _ in range(self.cell_count)]

        for cell in self.subjects_in_cells:
            x_sorted = sorted(cell, key=lambda s: s.get_particle_component().position_x)

            for i, subject in enumerate(x_sorted):
                if subject.already_in_quarantine:
                    subject.get_particle_component().update_location(timestamp)
                elif self.do_i_quarantine and (subject.get_infection_status(
                        timestamp) == InfectionStatuses.INFECTED or subject.on_my_way_to_quarantine):
                    self._quarantine_handler.guide_subject_journey(subject)
                    subject.get_particle_component().update_location_guided(timestamp)
                else:
                    if not subject.travelling:
                        chance = np.random.uniform(0, 1)
                        if chance < self.config.COMMUNITIES_VISIT_CHANCE:
                            self._community_handler.set_direction_to_destination(subject)
                            subject.get_particle_component().update_location_guided(timestamp)
                        else:
                            self._infection_handler.one_to_many(subject, x_sorted, i, timestamp)
                            subject.get_particle_component().update_location(timestamp)
                    else:
                        self._community_handler.guide_subject_journey(subject, timestamp)

                self.counts[subject.get_infection_status(timestamp).name].add(subject)
                new_cells[subject.cell_id].add(subject)
        self.subjects_in_cells = new_cells


if __name__ == "__main__":
    pass
