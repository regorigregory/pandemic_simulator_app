import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from models.MovingParticle import MovingParticle
import models.conf
import numpy as np
class MatplotlibBox():
    def __init__(self, cnf):
        self.config = cnf
        self.width = cnf.DIMENSIONS.value[0][1]
        self.height = cnf.DIMENSIONS.value[1][1]
    @property
    def width(self):
        return self._width
    @width.setter
    def width(self, x):
        self._width = x

    @property
    def height(self):
        return self._height

    @width.setter
    def height(self, y):
        self._height = y
    def init(self, n_particles):
        self.particles = [MovingParticle(self.config) for i in range(0, n_particles)]
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(0, self.width)
        self.ax.set_ylim(0, self.height)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.plot([p.position_x for p in self.particles], [p.position_y for p in self.particles], "ro")
    def update_locations_function(self):
        pass


if __name__ == "__main__":
    cnf = models.conf.Constants
    a_particle = MovingParticle(cnf)
    a_particle.get_acceleration_angle()
    a_box = MatplotlibBox(cnf)
    a_box.init(10)
