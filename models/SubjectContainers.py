from __future__ import annotations
from models.ConfigureMe import SubjectTypes, MainConfiguration
from models.Particle import Particle
from models.Subject import Subject
from models.InfectionHandlers import AxisBased
from models.CommutingHandlers import QuarantineHandler
import time
from abc import ABC, abstractmethod


class ContainerOfSubjects(ABC):
    def __init__(self):
        self.config = MainConfiguration()
        self._infection_handler = AxisBased()
        self.contents = set()
        self._particle_radius = self.config.SUBJECT_SIZE
        self._infection_radius = self.config.SUBJECT_INFECTION_RADIUS + self.config.SUBJECT_SIZE

    @abstractmethod
    def reset(self) -> None:
        pass

    @abstractmethod
    def populate_subjects(self) -> None:
        pass

    @abstractmethod
    def move_guys(self, timestamp: int) -> None:
        pass


class DefaultContainer(ContainerOfSubjects):
    def __init__(self):
        super().__init__()

        self.populate_subjects()
        self._infection_handler.count_them(0, self.contents)

        self.do_i_quarantine = self.config.QUARANTINE_MODE.get()
        if self.do_i_quarantine:
            self._quarantine_handler = QuarantineHandler()

    def reset(self):
        self = DefaultContainer()
        self._infection_handler.count_them(0, self.contents)

    def populate_subjects(self):
        constructor = Subject
        limit =  self.config.SUBJECT_NUMBER
        for i in range(0, limit):
            j = 0
            s = constructor(self.config)
            while(j < len(self.contents)):
                already_there = list(self.contents)[j]
                if s.are_we_too_close(already_there):
                    s = constructor(self.config)
                    j = 0
                else:
                    j += 1
            self.contents.add(s)
            #self.add_particle_to_grids(p)

    def move_guys(self, timestamp):
        self._infection_handler.many_to_many(timestamp)

        if not self.do_i_quarantine:

            for subject in self.contents:
                subject.get_particle_component().update_location()
        else:
            previous_immune_and_infected = self._infection_handler.counts["INFECTED"].union(self._infection_handler.counts["IMMUNE"])
            immune_and_infected = self._quarantine_handler.handle_infected_subjects(previous_immune_and_infected, timestamp)

            self._infection_handler.counts["INFECTED"] = immune_and_infected["INFECTED"]
            self._infection_handler.counts["IMMUNE"] = immune_and_infected["IMMUNE"]


            difference = self.contents - immune_and_infected["INFECTED"]
            difference = difference - immune_and_infected["IMMUNE"]

            for subject in difference:
                subject.get_particle_component().update_location()


class CommunitiesContainer(ContainerOfSubjects):
    def __init__(self):
        super().__init__()
        self.cell_count = self.config.COMMUNITIES_COLUMNS * self.config.COMMUNITIES_ROWS
        self.cell_dimensions = []
        self.subject_cells = [set() for i in range(self.cell_count)]

        self.init_cell_dimensions()

        self.populate_subjects()
        self._infection_handler.count_them(0, self.contents)

        self.do_i_quarantine = self.config.QUARANTINE_MODE.get()
        if self.do_i_quarantine:
            self._quarantine_handler = QuarantineHandler()

    def init_cell_dimensions(self):
        main_dimensions = self.config.get_particle_position_boundaries()
        full_width = main_dimensions[0][1] - main_dimensions[0][0]
        x_start = main_dimensions[0][0]

        full_height = main_dimensions[1][1]
        padding = self.config.INNER_PADDING
        rows = self.config.COMMUNITIES_ROWS
        columns = self.config.COMMUNITIES_COLUMNS
        row_height = full_height / rows - padding
        column_width = full_width / columns - padding
        patch_dimensions = dict(width=column_width - padding, height=row_height - padding)

        self.cell_dimensions = []
        for row in range(rows):
            for column in range(columns):
                x = x_start + padding + column * column_width
                y = padding + row * row_height
                width = patch_dimensions["width"]
                height = patch_dimensions["height"]
                self.cell_dimensions.append([[x, x + width], [y, y + height]])

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
            current_cell = self.subject_cells[c]
            s = constructor(self.config, boundaries=self.cell_dimensions[c])

            while j < len(current_cell):
                already_there = list(current_cell)[j]
                if s.are_we_too_close(already_there):
                    s = constructor(self.config, boundaries=self.cell_dimensions[c])
                    j = 0
                else:
                    j += 1

            current_cell.add(s)
            self.contents.add(s)

    def move_guys(self, timestamp):
        self._infection_handler.many_to_many(timestamp)

        if not self.do_i_quarantine:

            for subject in self.contents:
                subject.get_particle_component().update_location()
        else:
            previous_immune_and_infected = self._infection_handler.counts["INFECTED"].union(
                self._infection_handler.counts["IMMUNE"])
            immune_and_infected = self._quarantine_handler.handle_infected_subjects(previous_immune_and_infected,
                                                                                    timestamp)

            self._infection_handler.counts["INFECTED"] = immune_and_infected["INFECTED"]
            self._infection_handler.counts["IMMUNE"] = immune_and_infected["IMMUNE"]

            difference = self.contents - immune_and_infected["INFECTED"]
            difference = difference - immune_and_infected["IMMUNE"]

            for subject in difference:
                subject.get_particle_component().update_location()


if __name__ == "__main__":

    NUMBER_OF_TESTS = 1
    NUMBER_OF_SUBJECTS = range(100, 1000, 100)
    sequential = dict()
    parallel = dict()
    print('Evaluating Sequential Implementation...')

    for num_subjects in NUMBER_OF_SUBJECTS:
        box = DefaultContainer(MainConfiguration, number_of_subjects=num_subjects)
        if(num_subjects not in list(sequential.keys())):
            sequential[num_subjects] = 0.0000001
        for i in range(NUMBER_OF_TESTS):
            start = time.perf_counter_ns()
            box.move_guys(i)
            end = time.perf_counter_ns()- start
            sequential[num_subjects] += end
        sequential[num_subjects] /= NUMBER_OF_TESTS

    print('Evaluating Thread based Implementation...')

    for num_subjects in NUMBER_OF_SUBJECTS:
        box = DefaultContainer(MainConfiguration, number_of_subjects=num_subjects)
        if(num_subjects not in list(parallel.keys())):
            parallel[num_subjects] = 0.0000001
        for i in range(NUMBER_OF_TESTS):
            start = time.perf_counter()
            box.move_guys(i, parallel = True)
            end = time.perf_counter_ns() - start
            parallel[num_subjects] += end
        parallel[num_subjects] /= NUMBER_OF_TESTS

    for a, b in zip(sequential.items(), parallel.items()):
        print('Average Sequential Time for {} particles: {:.2f} ns'.format(a[0], a[1] * 1000*1000))
        print('Average Parallell Time for {} particles: {:.2f} ns'.format(b[0], b[1] * 1000*1000))
        print('Speedup: {:.2f} ns'.format(a[1] / b[1]))
        #print('Efficiency: {:.2f}%'.format(100 * (v1 / v2) / mp.cpu_count()))