import random
import math
from typing import NewType, List
import numpy as np
Vector = List[float]
VectorRange = List[List[float]]



class Particle:
    def __init__(self, cnf):
        self.position_vector = Particle.init_random_vector(cnf.DIMENSIONS.value)
        self.velocity_vector = Particle.init_random_vector(cnf.VELOCITY_RANGE.value)
        self.max_x = cnf.DIMENSIONS.value[0][1]
        self.max_y =  cnf.DIMENSIONS.value[1][1]

        self.min_x = cnf.DIMENSIONS.value[0][0]
        self.min_y = cnf.DIMENSIONS.value[1][0]
        self.radius = cnf.PARTICLE_RADIUS.value
        self.subject = None

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


    def update_location(self, rate_of_change = 1)->None:
        #self.velocity_vector = self.velocity_vector + self.acceleration_vector * rate_of_change
        self.position_vector = self.position_vector + self.velocity_vector * rate_of_change
        self.bounce_back_if_needed()


    def bounce_back_if_needed(self)->None:
        if self.position_x < 0:
            self.position_x = - self.position_x
            self.velocity_x = - self.velocity_x
        elif(self.position_x > self.max_x):
            self.position_x= 2 * self.max_x - self.position_x
            self.velocity_x = - self.velocity_x
        if self.position_y < 0:
            self.position_y = - self.position_y
            self.velocity_y = - self.velocity_y
        elif (self.position_y > self.max_y):
            self.position_y = 2 * self.max_y - self.position_y
            self.velocity_y = - self.velocity_y


    def have_we_encountered(self, other)->bool:
        #are we infecting each other
        #check if we have crossed paths!
        pass

    def should_we_socially_distance(self)->bool:
        #check if we should turn back
        #bounce back at the point of collision
        pass

    @staticmethod
    def init_random_vector(range:VectorRange)->Vector:
        x = np.random.uniform(*range[0])
        y = np.random.uniform(*range[1])
        return np.array([x,y])

if __name__ == "__main__":
    from models.conf import Constants
    testobject = Particle(Constants)
    testobject.position_x = -100
    testobject.velocity_x = -2
    testobject.update_location()
