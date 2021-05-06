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
        self.positions_by_status = {v: np.empty([0,2]) for v in self.count_keys}

        self.init_counts()
        self.r_rate = 0

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
        self.positions_by_status = {v: np.empty([0,2]) for v in self.count_keys}


    def count_them(self, timestamp=0):
        for s in self.contents:
            self.counts[s.get_infection_status(timestamp).name].add(s)

    @staticmethod
    def get_evenly_spaced_specs(bounds: list[list[float, float]], n: int = MainConfiguration().SUBJECT_NUMBER) \
            -> dict[str, float]:
        # thanks to mvw @
        # https://math.stackexchange.com/questions/1039482/how-to-evenly-space-a-number-of-points-in-a-rectangle

        w = bounds[0, 1] - bounds[0, 0]
        h = bounds[1, 1] - bounds[1, 0]
        n_x = ((w / h) * n + (w - h) ** 2 / (4 * (h ** 2))) ** 0.5 - (w - h) / (2 * h)
        n_y = n / n_x
        spacing = h / (n_y - 1)
        return dict(n_per_column=abs(n_x), n_per_row=abs(n_y), spacing=abs(spacing), w_h_ratio = w/h)

    @staticmethod
    def get_evenly_spaced_coordinates(i: int,
                                      bounds: list[list[float, float]],
                                      n_of_subjects: int = MainConfiguration().SUBJECT_NUMBER) \
            -> list[float, float]:

        dims = AbstractContainerOfSubjects.get_evenly_spaced_specs(bounds, n=n_of_subjects)
        row = int(i / dims["n_per_row"])
        column = i - (row * dims["n_per_row"])

        return [abs(column * dims["spacing"] * dims["w_h_ratio"]) + bounds[0,0], abs(row * dims["spacing"]) + bounds[1,0]]


class DefaultContainer(AbstractContainerOfSubjects):
    def __init__(self):
        super().__init__()
        self.subjects_in_cells = []
        self.rows = 2
        self.columns = 2
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
            position = AbstractContainerOfSubjects.get_evenly_spaced_coordinates(i, n_of_subjects=limit, bounds = self.config.get_particle_movement_bounds())
            s = constructor(position = position)

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
        try:
            cells[left][top].add(s)
            cells[right][top].add(s)
            cells[left][top].add(s)
            cells[right][bottom].add(s)
        except:
            print("Oooops")


    def move_guys(self, timestamp):

        self.init_counts()
        new_cells = [[set(), set()], [set(), set()]]
        self.r_rate = 0

        frames_per_day = self.config.get_frames_per_day()
        count_r = False
        if timestamp % frames_per_day == 0:
            count_r = True
            print("Going to count r!")

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
                    status_key = subject.get_infection_status(timestamp).name
                    """self.positions_by_status[status_key] = \
                        np.concatenate((self.positions_by_status[status_key], subject.get_particle_component().position_vector.reshape(1 , 2)), axis = 0 )
                    """
                    self.counts[status_key].add(subject)
                    if count_r:
                        self.r_rate += subject.estimate_total_infections(timestamp)

        if count_r:
            self.r_rate /= len(self.counts["INFECTED"]) + len(self.counts["ASYMPTOMATIC"])
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
            current_cell = self.subjects_in_cells[c]
            movement_boundaries = np.array(self.cell_coordinates[c])
            movement_boundaries[:, 0] += self.config.SUBJECT_SIZE
            movement_boundaries[:, 1] -= self.config.SUBJECT_SIZE
            position = AbstractContainerOfSubjects\
                .get_evenly_spaced_coordinates(i,
                                               n_of_subjects=limit,
                                               bounds=movement_boundaries)

            s = constructor(boundaries=movement_boundaries, position = position)
            s.cell_id = c
            current_cell.add(s)
            self.contents.add(s)

    def move_guys(self, timestamp):

        self.init_counts()
        new_cells = [set() for _ in range(self.cell_count)]
        self.r_rate = 0

        frames_per_day = self.config.get_frames_per_day()
        count_r = False
        if timestamp % frames_per_day == 0:
            count_r = True
            print("Going to count r!")

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

                status_key = subject.get_infection_status(timestamp).name
                """self.positions_by_status[status_key] = \
                    np.concatenate(
                        (self.positions_by_status[status_key], subject.get_particle_component().position_vector),
                        axis=0)"""
                self.counts[status_key].add(subject)
                new_cells[subject.cell_id].add(subject)
                if count_r:
                    self.r_rate += subject.estimate_total_infections(timestamp)
        if count_r:
            self.r_rate /= len(self.counts["INFECTED"]) + len(self.counts["ASYMPTOMATIC"])
        self.subjects_in_cells = new_cells


if __name__ == "__main__":
    pass
