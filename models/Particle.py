from __future__ import annotations
import math
from typing import NewType, List
from models.ConfigureMe import MainConfiguration
import numpy as np
Vector = List[float]
VectorRange = List[List[float]]


class Particle:
    def __init__(self, cnf = MainConfiguration()):
        self.position_vector = Particle.init_random_vector(cnf.get_main_subjects_box_dimensions())
        self.velocity_vector = np.random.uniform(*cnf.SUBJECT_VELOCITY, [2,])
        self.max_x, self.max_y = cnf.get_dimensions("SimulationFrame")

        self.last_location_update = -1
        self.min_x = 0
        self.min_y = 0
        self._radius = cnf.SUBJECT_SIZE
        self.subject = None

    def get_radius(self):
        return self._radius

    def get_particle_component(self):
        return self



    @property
    def position_vector(self):
        return self._position_vector

    @position_vector.setter
    def position_vector(self, value):
        self._position_vector = np.array(value)

    @property
    def position_x(self):
        return self._position_vector[0]

    @position_x.setter
    def position_x(self, x):
        self._position_vector[0] = x

    @property
    def position_y(self):
        return self._position_vector[1]

    @position_y.setter
    def position_y(self, y):
        self._position_vector[1] = y


    @property
    def velocity_vector(self):
        return self._velocity_vector
    @velocity_vector.setter
    def velocity_vector(self, values):
        self._velocity_vector = np.array(values)

    @property
    def velocity_x(self):
        return self._velocity_vector[0]

    @velocity_x.setter
    def velocity_x(self, value):
        self._velocity_vector[0] = value

    @property
    def velocity_y(self):
        return self._velocity_vector[1]

    @velocity_y.setter
    def velocity_y(self, value):
        self._velocity_vector[1] = value


    def update_location(self, rate_of_change = 1) -> None:
        #self.velocity_vector = self.velocity_vector + self.acceleration_vector * rate_of_change

        self.position_vector = self.position_vector + self.velocity_vector * rate_of_change
        self.bounce_back_if_needed()

    def bounce_back_if_needed(self) -> None:
        if self.position_x < self.min_x:
            self.position_x = - self.position_x
            self.velocity_x = - self.velocity_x

        elif self.position_x > self.max_x:
            self.position_x= 2 * self.max_x - self.position_x
            self.velocity_x = - self.velocity_x

        if self.position_y < self.min_y:
            self.position_y = - self.position_y
            self.velocity_y = - self.velocity_y
        elif self.position_y > self.max_y:
            self.position_y = 2 * self.max_y - self.position_y
            self.velocity_y = - self.velocity_y


    @staticmethod
    def init_random_vector(range: VectorRange) -> Vector:
        x = np.random.uniform(*range[0])
        y = np.random.uniform(*range[1])
        return np.array([x,y])

    def rotate_velocity(self, angle) -> Particle:
        new_x_velocity = self.velocity_x * np.cos(angle) + self.velocity_y * np.sin(angle)
        self.velocity_y = - self.velocity_x * np.sin(angle) + self.velocity_y * np.cos(angle)
        self.velocity_x = new_x_velocity
        return self.velocity_vector


if __name__ == "__main__":

    from models.ConfigureMe import MainConfiguration
    testobject = Particle(MainConfiguration)
    testobject.position_x = -100
    testobject.velocity_x = -2
    testobject.update_location()
