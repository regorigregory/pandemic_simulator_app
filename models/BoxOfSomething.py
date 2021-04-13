from models.conf import SubjectTypes, Constants
from models.Particle import Particle
from models.Subject import Subject
from models.InfectionHandlers import InfectionHandlerInterface
import math
import numpy as np
class Box:
    def __init__(self, config):
        self.contents = []
        self._gridsize = (config.INFECTION_RADIUS.value + config.PARTICLE_RADIUS.value) * config.SUBJECTS_PER_GRID.value
        self._n_horizontal_grids = math.ceil(config.DIMENSIONS.value[0][1] / self._gridsize)
        self._n_vertical_grids = math.ceil(config.DIMENSIONS.value[1][1] / self._gridsize)
        self._n_grids = self._n_vertical_grids * self._n_horizontal_grids
        self._particle_radius= config.PARTICLE_RADIUS

        self._infection_radius = config.INFECTION_RADIUS.value + config.PARTICLE_RADIUS.value
        self.populate_subjects(config)

    def init_grids(self):
        self._grids = np.array([set() for _ in range(self._n_grids)])\
            .reshape(self._n_vertical_grids, self._n_horizontal_grids)

    def populate_subjects(self, config):
        self.init_grids()
        if config.SUBJECT_TYPE.value == SubjectTypes.PARTICLE:
            constructor = Particle
        else:
            constructor = Subject
        for i in range(0, config.NUMBER_OF_SUBJECTS.value):
            p = constructor(config)
            self.contents.append(p)
            #self.add_particle_to_grids(p)

    def add_particle_to_grids(self, particle):
        x, y = particle.get_particle_component().position_x,\
               particle.get_particle_component().position_y,
        for i in range(-1, 2):

            x_temp = int((x + i * self._infection_radius) / self._gridsize)

            if 0 <= x_temp < self._n_horizontal_grids:
                for j in range(-1, 2):

                    y_temp = int((y + j * self._infection_radius) / self._gridsize)

                    if 0 <= y_temp < self._n_vertical_grids:
                        self._grids[y_temp, x_temp,].add(particle)


    def move_guys(self, timestamp, infection_handler: InfectionHandlerInterface = None):
        for particle in self.contents:
            particle.get_particle_component().update_location()
            #self.add_particle_to_grids(particle)
        if (infection_handler is not None):
            infection_handler.many_to_many(timestamp, [self.contents])
if __name__ == "__main__":
    box = Box(Constants)