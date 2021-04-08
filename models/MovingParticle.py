Vector = list[float]
VectorRange = list[list[float]]
import random
import math
from conf import Constants as cnf
from conf import Edges as edge

class MovingParticle():
    def __init__(self, cnf):
        self.position_vector = MovingParticle.init_random_vector(cnf.DIMENSIONS)
        self.velocity_vector = MovingParticle.init_random_vector(cnf.VELOCITY_RANGE)
        self.acceleration_vector = MovingParticle.init_random_vector(cnf.ACCELERATION_RANGE)
        self.max_x = cnf.DIMENSIONS[0][1]
        self.max_y =  cnf.DIMENSIONS[1][1]

        self.min_x = cnf.DIMENSIONS[0][0]
        self.min_y = cnf.DIMENSIONS[1][0]
        self.radius = cnf.PARTICLE_RADIUS

    @staticmethod
    def init_random_vector(range:VectorRange)->Vector:
        x = random.uniform(*VectorRange[0])
        y = random.uniform(*VectorRange[1])
        return [x,y]
    def _get_vector_angle(self, vector:Vector)->float:
        return math.atan(vector[1]/vector[0])
    def _get_vector_magnitude(self, vector:Vector)->float:
        return math.sqrt(vector[0]**2 + vector[1]**2)

    def get_velocity_angle(self)->float:
        return self._get_vector_angle(self.velocity_vector)
    def get_position_angle(self)->float:
        return self._get_vector_angle(self.position_vector)
    def get_acceleration_angle(self)->float:
        return self._get_vector_angle(self.acceleration_vector)

    def _is_horizontal_edge(self)->bool:
        if (self.position_vector[0] - self.radius <= self.min_x or self.position_vector[0] + self.radius >= self.max_x):
            return True
        return False

    def _is_vertical_edge(self)->bool:
        if (self.position_vector[1] - self.radius <= self.min_y or self.position_vector[1] + self.radius >= self.max_y):
            return True
        return False

    def update_location(self, rate_of_change = 1)->None:
        self.edge_safe_direction_update()
        self.velocity_vector = self.velocity + self.acceleration * rate_of_change
        self.position_vector = self.position_vector + self.velocity_vector * rate_of_change

    def edge_safe_direction_update(self)->None:
        if(self._is_horizontal_edge()):
            self.velocity_vector[0] = -1 * self.velocity_vector[0]
        if (self._is_vertical_edge()):
            self.velocity_vector[1] = -1 * self.velocity_vector[1]
