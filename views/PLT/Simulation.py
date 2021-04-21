import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, Animation, TimedAnimation

from models.SubjectContainers import BoxOfSubjects
from matplotlib.widgets import Button
from models.ConfigureMe import Constants
import numpy as np


class ObserverClient(object):
    def __init__(self):
        self.observers = []

    def attach(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def detach(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def notify(self, data):
        for observer in self.observers:
            observer.update(data)


class MovingSubjects(ObserverClient):
    def __init__(self, config=Constants(), container=None):
        super().__init__()
        self.config = config
        self.width, self.height = config.get_dimensions(1, "SIMULATION_DIM")
        self.DPI = config.DPI

        self._marker_radius = config.PARTICLE_RADIUS
        self._infection_zone_radius = config.INFECTION_RADIUS + config.PARTICLE_RADIUS

        self._box_of_particles = container

        self.fig = plt.figure(figsize=(self.width / self.DPI, self.height / self.DPI), dpi=self.DPI)
        self._infection_handler = self._box_of_particles._infection_handler
        self.ax = plt.gca()

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

    def get_current_coordinates(self, subjects):

        return np.array([[p.get_particle_component().position_x for p in subjects],
                         [p.get_particle_component().position_y for p in subjects]])

    def move_guys(self, i):
        self._box_of_particles.move_guys(i)

    def get_init_func(self):
        self.ax.set_xlim(0, self.width)
        self.ax.set_ylim(0, self.height)
        self._infection_handler.count_them(0, self._box_of_particles.contents)
        self.notify(self._infection_handler.counts)

        self.ax.set_xticks([])
        self.ax.set_yticks([])

        # immune
        self.ax.plot(*self.get_current_coordinates(self._infection_handler.counts["IMMUNE"]), marker=".",
                     fillstyle="full", linestyle="", color="blue", markersize=self._marker_radius * 2)

        # susceptible

        self.ax.plot(*self.get_current_coordinates(self._infection_handler.counts["SUSCEPTIBLE"]), marker=".",
                     fillstyle="full", linestyle="", color="orange", markersize=self._marker_radius * 2)

        # infected
        INFECTED_COORDS = self.get_current_coordinates(self._infection_handler.counts["INFECTED"])

        self.ax.plot(*INFECTED_COORDS, marker=".",
                     fillstyle="full", linestyle="", color="red", markersize=self._marker_radius * 2)

        self.ax.plot(*INFECTED_COORDS, marker=".", fillstyle="none", color="red", linestyle="",
                     markersize=self._infection_zone_radius * 2)

        def func():
            return self.ax.lines[0], self.ax.lines[1], self.ax.lines[2], self.ax.lines[3]

        return func

    def get_animation_function(self):
        def func(i):
            self.move_guys(i)
            self._infection_handler.count_them(i, self._box_of_particles.contents)
            self.notify(self._infection_handler.counts)

            INFECTED_COORDS = self.get_current_coordinates(self._infection_handler.counts["INFECTED"])
            IMMUNE_COORDS = self.get_current_coordinates(self._infection_handler.counts["IMMUNE"])
            SUSCEPTIBLE_COORDS = self.get_current_coordinates(self._infection_handler.counts["SUSCEPTIBLE"])

            self.ax.lines[0].set_data(*IMMUNE_COORDS)
            self.ax.lines[1].set_data(*SUSCEPTIBLE_COORDS)
            self.ax.lines[2].set_data(*INFECTED_COORDS)
            self.ax.lines[3].set_data(*INFECTED_COORDS)

            # self._infection_handler.print_counts()
            return self.ax.lines[0], self.ax.lines[1], self.ax.lines[2], self.ax.lines[3]

        return func

    def start_animation(self):
        init_func = self.get_init_func()
        animation_function = self.get_animation_function()

        anim = FuncAnimation(self.fig,
                             animation_function,
                             init_func=init_func,
                             interval=20)
        return anim

    def reset(self):
        self._box_of_particles.reset()
        self._infection_handler = self._box_of_particles._infection_handler
        plt.cla()
        plt.clf()
        self.ax = plt.gca()


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    plt.ioff()
    ViewBox = MovingSubjects(container=BoxOfSubjects())
    a = ViewBox.start_animation()
    plt.show()
    """init_func = ViewBox.get_init_func()
    animation_function = ViewBox.get_animation_function()

    anim = FuncAnimation(ViewBox.fig,
                         animation_function,
                         init_func = init_func,
                         interval=20)"""
