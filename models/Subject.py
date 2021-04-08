import random
import math
class Subject():
    def __init__(self, config, am_i_infected = False):
        self._infection_radius = Subject.set_random_attribute_safely(config.INFECTION_RADIUS)
        self._recovery_time = Subject.set_random_attribute_safely(config.INFECTION_RADIUS)
        self._incubation_period = Subject.set_random_attribute_safely(config.INFECTION_RADIUS)
        self._infection_probability = Subject.set_random_attribute_safely(config.INFECTION_RADIUS)
        self._location_x = Subject.set_random_attribute_safely([0, config.GRID_WIDTH])
        self._location_y = Subject.set_random_attribute_safely([0, config.GRID_HEIGHT])
        self.direction_angle = random.uniform(0, 2 * math.pi)
        self.speed = 1
        if(am_i_infected):
            self.start_of_infection = 1
        else:
            self.start_of_infection = 0

    def update_location(self):
        d_x = math.cos(self.direction_angle) * self.speed
        d_y = math.sin(self.direction_angle) * self.speed
        self.location_x += int(d_x)
        self.location_y += int(d_y)
        
    def reverse_direction(self):
        self.direction_angle = self.direction_angle + 2 * math.pi
    def will_i_infect_you(self, timestamp: int):
        if(self.am_i_infectious(timestamp)):
            return random.random() > self._infection_probability
        return False

    def infect_at(self, timestamp: int):
        self.start_of_infection = timestamp

    def am_i_infectious(self, timestamp: int):
        if(self.start_of_infection == 0 or self.have_i_recovered(timestamp)):
            return False
        return True

    def have_i_recovered(self, timestamp: int):
        if timestamp - self.start_of_infection > self._recovery_time:
            return True
        return False

    @staticmethod
    def set_random_attribute_safely(const_or_arr):
        if isinstance(const_or_arr, list):
            return random.uniform(*const_or_arr)
        return const_or_arr

if __name__ == "__main__":
    pass