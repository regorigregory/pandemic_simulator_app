import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from models.BoxOfSomething import Box
from models.Particle import Particle
from models.conf import Constants
from models.InfectionHandlers import Naive

import numpy as np

class BoxView():
    def __init__(self, cnf, infection_handler = Naive()):
        self.config = cnf
        self.width = cnf.DIMENSIONS.value[0][1]
        self.height = cnf.DIMENSIONS.value[1][1]
        self.DPI = cnf.DPI.value
        self._infection_handler = infection_handler
        self._marker_radius = cnf.PARTICLE_RADIUS.value
        self._infection_zone_radius = cnf.INFECTION_RADIUS.value + cnf.PARTICLE_RADIUS.value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, x):
        self._width = x

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, y):
        self._height = y


    def get_current_coordinates(self):
        return np.array([[p.get_particle_component().position_x for p in self._box_of_particles.contents],
                         [p.get_particle_component().position_y for p in self._box_of_particles.contents]])

    def move_guys(self, i):
        self._box_of_particles.move_guys(i, infection_handler = self._infection_handler)

    def get_init_func(self, BoxOfParticles):
        self._box_of_particles = BoxOfParticles
        self.fig = plt.figure(figsize = (self.width/self.DPI, self.height/self.DPI), dpi=self.DPI)
        self.ax = plt.gca()
        self.ax.set_xlim(0, self.width)
        self.ax.set_ylim(0, self.height)
        #self.ax.set_xticks([])
        #self.ax.set_yticks([])
        self.ax.plot(*self.get_current_coordinates(), marker = ".", fillstyle = "full", linestyle = "", markersize = self._marker_radius * 2)
        self.ax.plot(*self.get_current_coordinates(), marker = ".", fillstyle = "none", color = "red", linestyle = "", markersize = self._infection_zone_radius * 2)

        def func():
            return self.ax.lines[0], self.ax.lines[1]
        return func

    def get_animation_function(self):
        def func(i):
            self.move_guys(i)
            self.ax.lines[0].set_data(*self.get_current_coordinates())
            self.ax.lines[1].set_data(*self.get_current_coordinates())

            self._infection_handler.print_counts()
            return self.ax.lines[0], self.ax.lines[1]
        return func

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from models.conf import Constants

    cnf = Constants
    ParticleBox = Box(cnf)
    InfectionHanlder = Naive()

    ViewBox = BoxView(cnf)
    init_func = ViewBox.get_init_func(ParticleBox)
    animation_function = ViewBox.get_animation_function()


    anim = FuncAnimation(ViewBox.fig,
                         animation_function,
                         init_func = init_func,
                         frames=300,
                         interval=20)
