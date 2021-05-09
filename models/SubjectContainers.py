from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np
from models.AbstractClasses import AbstractContainerOfSubjects
from models.ConfigureMe import InfectionStatuses, MainConfiguration
from models.MovementHandlers import QuarantineHandler, CommunityHandler
from models.Subject import Subject


class DefaultContainer(AbstractContainerOfSubjects):
    def __init__(self):
        super().__init__()
        self.subjects_in_cells = []
        self.rows = 6
        self.columns = 12
        self.cell_count = self.rows * self.columns
        self.init_cells()

        self.populate_subjects()
        self.do_i_quarantine = MainConfiguration().QUARANTINE_MODE.get()
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
        limit = MainConfiguration().SUBJECT_NUMBER
        for i in range(0, int(limit)):
            j = 0
            position = AbstractContainerOfSubjects.get_evenly_spaced_coordinates(i, n_of_subjects=limit, bounds = MainConfiguration().get_particle_movement_bounds())
            s = constructor(position=position)

            self.contents.add(s)

            self.add_subject_to_cell(s, self.subjects_in_cells)

    def add_subject_to_cell(self, s: Subject, cells: list[set[Subject]] = None):

        subject_radius = MainConfiguration().SUBJECT_SIZE + MainConfiguration().SUBJECT_INFECTION_RADIUS
        left = int((s.get_particle_component().position_vector[0] - subject_radius)
                   / (MainConfiguration().MAIN_CANVAS_SIZE[0] / self.columns))
        right = int((s.get_particle_component().position_vector[0] + subject_radius)
                    / (MainConfiguration().MAIN_CANVAS_SIZE[0] / self.columns))
        bottom = int((s.get_particle_component().position_vector[1] - subject_radius)
                     / (MainConfiguration().MAIN_CANVAS_SIZE[1] / self.rows))
        top = int((s.get_particle_component().position_vector[1] + subject_radius) / (
                MainConfiguration().MAIN_CANVAS_SIZE[1] / self.rows))

        top = top if top < self.rows else self.rows-1
        bottom = bottom if bottom >= 0 else 0
        right = right if right < self.columns else self.columns - 1
        left = left if left >= 0 else 0

        try:
            cells[top][left].add(s)
            cells[top][right].add(s)
            cells[bottom][left].add(s)
            cells[bottom][right].add(s)
        except:
            print("Oooops")


    def move_guys(self, timestamp):

        self.init_counts()
        new_cells = [[set() for _ in range(self.columns)] for _ in range(self.rows)]
        self.r_rate = 0

        frames_per_day = MainConfiguration().get_frames_per_day()
        count_r = False
        if timestamp % frames_per_day == 0:
            count_r = True
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
                    #self.positions_by_status[status_key][0].append(int(subject.get_particle_component().position_vector[0]))
                    #self.positions_by_status[status_key][1].append(int(subject.get_particle_component().position_vector[1]))

                    self.counts[status_key].add(subject)
                    if count_r:
                        self.r_rate += subject.estimate_total_infections(timestamp)

        if count_r:
            divisor = len(self.counts["INFECTED"]) + len(self.counts["ASYMPTOMATIC"])

            self.r_rate = self.r_rate / divisor if divisor > 0 else 0
        self.subjects_in_cells = new_cells


class CommunitiesContainer(AbstractContainerOfSubjects):
    def __init__(self):
        super().__init__()
        self.cell_count = MainConfiguration().COMMUNITIES_COLUMNS * MainConfiguration().COMMUNITIES_ROWS
        self.cell_coordinates = MainConfiguration().get_community_cells_border_bounds()
        self.subjects_in_cells = [set() for _ in range(self.cell_count)]
        self.populate_subjects()
        self._community_handler = CommunityHandler()

        self.do_i_quarantine = MainConfiguration().QUARANTINE_MODE.get()
        if self.do_i_quarantine:
            self._quarantine_handler = QuarantineHandler()

    def reset(self):
        self = CommunitiesContainer()

    def populate_subjects(self):
        limit = int(MainConfiguration().SUBJECT_NUMBER / self.cell_count)
        remainder = MainConfiguration().SUBJECT_NUMBER - self.cell_count * limit

        for c in range(self.cell_count):
            self.populate_cell(c, limit)
        self.populate_cell(c, remainder)

    def populate_cell(self, c, limit):
        constructor = Subject
        for i in range(limit):
            current_cell = self.subjects_in_cells[c]
            movement_boundaries = np.array(self.cell_coordinates[c])
            movement_boundaries[:, 0] += MainConfiguration().SUBJECT_SIZE
            movement_boundaries[:, 1] -= MainConfiguration().SUBJECT_SIZE
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

        frames_per_day = MainConfiguration().get_frames_per_day()
        count_r = False
        if timestamp % frames_per_day == 0:
            count_r = True

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
                        if chance < MainConfiguration().COMMUNITIES_VISIT_CHANCE/1000:
                            self._community_handler.set_direction_to_destination(subject)
                            subject.get_particle_component().update_location_guided(timestamp)
                        else:
                            self._infection_handler.one_to_many(subject, x_sorted, i, timestamp)
                            subject.get_particle_component().update_location(timestamp)
                    else:
                        self._community_handler.guide_subject_journey(subject, timestamp)

                status_key = subject.get_infection_status(timestamp).name
                #self.positions_by_status[status_key][0].append(int(subject.get_particle_component().position_vector[0]))
                #self.positions_by_status[status_key][1].append(int(subject.get_particle_component().position_vector[1]))

                """self.positions_by_status[status_key] = \
                    np.concatenate(
                        (self.positions_by_status[status_key], subject.get_particle_component().position_vector),
                        axis=0)"""
                self.counts[status_key].add(subject)
                new_cells[subject.cell_id].add(subject)
                if count_r:
                    self.r_rate += subject.estimate_total_infections(timestamp)
        if count_r:
            divisor = len(self.counts["INFECTED"]) + len(self.counts["ASYMPTOMATIC"])

            self.r_rate = self.r_rate / divisor if divisor > 0 else 0
        self.subjects_in_cells = new_cells


if __name__ == "__main__":
    pass
