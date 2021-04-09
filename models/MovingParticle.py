import random
import math
from typing import NewType, List
import numpy as np
Vector = List[float]
VectorRange = List[List[float]]



class MovingParticle():
    def __init__(self, cnf):
        self.position_vector = MovingParticle.init_random_vector(cnf.DIMENSIONS.value)
        self.velocity_vector = MovingParticle.init_random_vector(cnf.VELOCITY_RANGE.value)
        self.acceleration_vector = MovingParticle.init_random_vector(cnf.ACCELERATION_RANGE.value)
        self.max_x = cnf.DIMENSIONS.value[0][1]
        self.max_y =  cnf.DIMENSIONS.value[1][1]

        self.min_x = cnf.DIMENSIONS.value[0][0]
        self.min_y = cnf.DIMENSIONS.value[1][0]
        self.radius = cnf.PARTICLE_RADIUS.value

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
    @position_x.setter
    def position_x(self, y):
        self._position_vector[1] = y


    @property
    def velocity_vector(self):
        return self._velocity_vector
    @position_vector.setter
    def velocity_vector(self, value):
        self._velocity_vector = np.array(value)

    @property
    def acceleration_vector(self):
        return self._acceleration_vector
    @acceleration_vector.setter
    def acceleration_vector(self, value):
        self._acceleration_vector =  np.array(value)

    def _get_vector_angle(self, attribute_name)->float:
        dict_of_attributes: dict = self.__dict__
        try:
            if attribute_name in list(dict_of_attributes.keys()):
                perhaps_vector = dict_of_attributes.get(attribute_name)
                if isinstance(perhaps_vector, np.ndarray):
                    return math.atan(perhaps_vector[1] / perhaps_vector[0])
                else:
                    raise Exception("The requested attribute is not a vector. Cannot calculate angle.")
            else:
                raise Exception("The requested attribute is not an atrribute.")
        except Exception as e:
            print(e)




    def _get_vector_magnitude(self, vector:Vector)->float:
        return math.sqrt(vector[0]**2 + vector[1]**2)

    def get_velocity_angle(self)->float:
        return self._get_vector_angle("_velocity_vector")
    def get_position_angle(self)->float:
        return self._get_vector_angle("_position_vector")
    def get_acceleration_angle(self)->float:
        return self._get_vector_angle("_acceleration_vector")

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
        self.velocity_vector = self.velocity_vector + self.acceleration_vector * rate_of_change
        self.position_vector = self.position_vector + self.velocity_vector * rate_of_change

    def edge_safe_direction_update(self)->None:
        if(self._is_horizontal_edge()):
            self.velocity_vector[0] = -1 * self.velocity_vector[0]
        if (self._is_vertical_edge()):
            self.velocity_vector[1] = -1 * self.velocity_vector[1]
    @staticmethod
    def init_random_vector(range:VectorRange)->Vector:
        x = random.uniform(*range[0])
        y = random.uniform(*range[1])
        return [x,y]
if __name__ == "__main__":
    pass
