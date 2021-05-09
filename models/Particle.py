from __future__ import annotations
from typing import Union

import numpy as np

from models.ConfigureMe import MainConfiguration


class Particle:
    def __init__(self, boundaries=None, position = None):
        bounding_box = MainConfiguration().get_particle_movement_bounds() if boundaries is None else boundaries
        if position is None:
            self.position_vector = Particle.init_random_vector(bounding_box)
        else:
            self.position_vector = position

        self.min_x = 0
        self.max_x = 0
        self.min_y = 0
        self.max_y = 0

        self.set_boundaries(bounding_box)
        self.velocity_vector = np.random.uniform(*MainConfiguration().SUBJECT_VELOCITY, [2, ])

        self.last_location_update = -1

        self._radius = MainConfiguration().SUBJECT_SIZE
        self.subject = None
        self.quarantine_mode = MainConfiguration().QUARANTINE_MODE

    def set_boundaries(self, bounding_box: list[list[float]]) -> None:
        self.min_x = bounding_box[0][0]
        self.max_x = bounding_box[0][1]
        self.min_y = bounding_box[1][0]
        self.max_y = bounding_box[1][1]

    def get_radius(self) -> float:
        return self._radius

    def get_particle_component(self) -> Particle:
        return self

    @property
    def position_vector(self) -> np.ndarray:
        return self._position_vector

    @position_vector.setter
    def position_vector(self, value: Union[list, np.ndarray]) -> None:
        self._position_vector = np.array(value)

    @property
    def position_x(self) -> float:
        return self._position_vector[0]

    @position_x.setter
    def position_x(self, x: float) -> None:
        self._position_vector[0] = x

    @property
    def position_y(self) -> float:
        return self._position_vector[1]

    @position_y.setter
    def position_y(self, y: float) -> None:
        self._position_vector[1] = y

    @property
    def velocity_vector(self) -> np.ndarray:
        return self._velocity_vector

    @velocity_vector.setter
    def velocity_vector(self, values: Union[list[float], np.ndarray[float]]) -> None:
        self._velocity_vector = np.array(values) / 30

    @property
    def velocity_x(self) -> float:
        return self._velocity_vector[0]

    @velocity_x.setter
    def velocity_x(self, value: float) -> None:
        self._velocity_vector[0] = value

    @property
    def velocity_y(self) -> float:
        return self._velocity_vector[1]

    @velocity_y.setter
    def velocity_y(self, value: float) -> None:
        self._velocity_vector[1] = value

    def update_location(self, timestamp: int) -> None:
        if self.last_location_update == timestamp:
            return
        self.last_location_update = timestamp
        self.position_vector = self.position_vector + self.velocity_vector * MainConfiguration().SUBJECT_VELOCITY_MULTIPLIER
        self.bounce_back_if_needed()

    def update_location_guided(self, timestamp: int, rate_of_change=1) -> None:
        if self.last_location_update == timestamp:
            return
        self.last_location_update = timestamp
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
    def init_random_vector(range_: Union[np.ndarray, list[list[float]]]) -> np.ndarray[float]:
        x = np.random.uniform(*range_[0])
        y = np.random.uniform(*range_[1])
        return np.array([x, y])

    def rotate_velocity(self, angle: float) -> np.ndarray:
        new_x_velocity = self.velocity_x * np.cos(angle) + self.velocity_y * np.sin(angle)
        self.velocity_y = - self.velocity_x * np.sin(angle) + self.velocity_y * np.cos(angle)
        self.velocity_x = new_x_velocity
        return self.velocity_vector

    def resolve_collision(self, other_particle: Particle) -> None:
        particle = self
        x_velocity_diff = particle.velocity_x - other_particle.velocity_x
        y_velocity_diff = particle.velocity_y - other_particle.velocity_y

        x_dist = other_particle.position_x - particle.position_x
        y_dist = other_particle.position_y - particle.position_y

        if x_velocity_diff * x_dist + y_velocity_diff * y_dist >= 0:

            angle = np.arctan2(other_particle.position_y - particle.position_y,
                               other_particle.position_x - particle.position_x)
            u1 = particle.rotate_velocity(angle) * 30
            u2 = other_particle.rotate_velocity(angle) * 30

            # one dimensional Newtonian
            # since each particle's mass == 1, the equation has been simplified
            # https://en.wikipedia.org/wiki/Elastic_collision#:~:text=One%2Ddimensional%20Newtonian,-Play%20media&text=This%20simply%20corresponds%20to%20the,reference%20with%20constant%20translational%20velocity.

            particle.velocity_vector = [u2[0], u1[1]]
            other_particle.velocity_vector = [u1[0], u2[1]]
            particle.rotate_velocity(-angle)
            other_particle.rotate_velocity(-angle)


if __name__ == "__main__":
    from models.ConfigureMe import MainConfiguration

    testobject = Particle(MainConfiguration)
    testobject.position_x = -100
    testobject.velocity_x = -2
    testobject.update_location()
