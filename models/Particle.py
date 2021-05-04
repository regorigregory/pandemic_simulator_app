from __future__ import annotations
from typing import Union

import numpy as np

from models.ConfigureMe import MainConfiguration


class Particle:
    def __init__(self, cnf=MainConfiguration(), boundaries=None):
        bounding_box = cnf.get_main_simulation_canvas_movement_bounds_for_particles() if boundaries is None else boundaries

        self.position_vector = Particle.init_random_vector(bounding_box)
        self.min_x = 0
        self.max_x = 0
        self.min_y = 0
        self.max_y = 0

        self.set_boundaries(bounding_box)
        self.velocity_vector = np.random.uniform(*cnf.SUBJECT_VELOCITY, [2, ])

        self.last_location_update = -1

        self._radius = cnf.SUBJECT_SIZE
        self.subject = None
        self.quarantine_mode = MainConfiguration().QUARANTINE_MODE

    def set_boundaries(self, bounding_box: list[list[float]]):
        self.min_x = bounding_box[0][0]
        self.max_x = bounding_box[0][1]
        self.min_y = bounding_box[1][0]
        self.max_y = bounding_box[1][1]

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

    def update_location(self, rate_of_change=1) -> None:

        self.position_vector = self.position_vector + self.velocity_vector * rate_of_change
        self.bounce_back_if_needed()

    def update_location_guided(self, rate_of_change=1) -> None:

        self.position_vector = self.position_vector + self.velocity_vector * rate_of_change

    def bounce_back_if_needed(self) -> None:
        if self.position_x < self.min_x:
            self.position_x = self.min_x + 1
            self.velocity_x = - self.velocity_x

        elif self.position_x > self.max_x:
            self.position_x = 2 * self.max_x - self.position_x
            self.velocity_x = - self.velocity_x

        if self.position_y < self.min_y:
            self.position_y = self.min_y + 1
            self.velocity_y = - self.velocity_y

        elif self.position_y > self.max_y:
            self.position_y = 2 * self.max_y - self.position_y
            self.velocity_y = - self.velocity_y

    @staticmethod
    def init_random_vector(range_: list[list[float]]) -> np.array[float]:
        x = np.random.uniform(*range_[0])
        y = np.random.uniform(*range_[1])
        return np.array([x, y])

    def rotate_velocity(self, angle) -> Particle:
        new_x_velocity = self.velocity_x * np.cos(angle) + self.velocity_y * np.sin(angle)
        self.velocity_y = - self.velocity_x * np.sin(angle) + self.velocity_y * np.cos(angle)
        self.velocity_x = new_x_velocity
        return self.velocity_vector

    def resolve_collision(self, otherParticle: Particle):
        particle = self
        # x_velocity_diff = particle.velocity_x - otherParticle.velocity_x
        # y_velocity_diff = particle.velocity_y - otherParticle.velocity_y

        # x_dist = otherParticle.position_x - particle.position_x
        # y_dist = otherParticle.position_y - particle.position_y

        if True:  # x_velocity_diff * x_dist + y_velocity_diff * y_dist >= 0:

            angle = np.arctan2(otherParticle.position_y - particle.position_y,
                               otherParticle.position_x - particle.position_x)
            u1 = particle.rotate_velocity(angle)
            u2 = otherParticle.rotate_velocity(angle)

            # one dimensional Newtonian
            # since each particle's mass == 1, the equation has been simplified
            # https://en.wikipedia.org/wiki/Elastic_collision#:~:text=One%2Ddimensional%20Newtonian,-Play%20media&text=This%20simply%20corresponds%20to%20the,reference%20with%20constant%20translational%20velocity.

            particle.velocity_vector = [u2[0], u1[1]]
            otherParticle.velocity_vector = [u1[0], u2[1]]
            particle.rotate_velocity(-angle)
            otherParticle.rotate_velocity(-angle)


if __name__ == "__main__":
    from models.ConfigureMe import MainConfiguration

    testobject = Particle(MainConfiguration)
    testobject.position_x = -100
    testobject.velocity_x = -2
    testobject.update_location()
