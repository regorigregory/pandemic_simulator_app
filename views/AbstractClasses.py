from tkinter import Frame
from abc import ABC, abstractmethod
from models.ConfigureMe import MainConfiguration, Theme
from models.SubjectContainers import *
import numpy as np


class AbstractSimulation(ABC):
    def __init__(self, config = MainConfiguration()):
        super().__init__()
        self.config = config
        self.theme = Theme()
        self.width, self.height = config.get_frame_dimensions_of("SimulationFrame")
        self._marker_radius = config.SUBJECT_SIZE
        self._infection_zone_radius = config.SUBJECT_INFECTION_RADIUS + config.SUBJECT_SIZE
        #self._box_of_particles = CommunitiesContainer() if self.config.COMMUNITY_MODE.get() else DefaultContainer()
        self.previous_infected = 0
        self.previous_r = 0

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

    @abstractmethod
    def resume(self):
        pass

    @abstractmethod
    def pause(self):
        pass

    @abstractmethod
    def start_animation(self):
        pass

    @abstractmethod
    def reset(self):
        pass


class AbstractFrame(Frame):
    def __init__(self, root, config=MainConfiguration()):
        self.config = config
        self.dim_dict = {"width": (self.config.get_frame_dimensions_of(self.__class__.__name__))[0],
                         "height": (self.config.get_frame_dimensions_of(self.__class__.__name__))[1]}
        self.frame_settings = self.config.FRAME_SETTINGS[self.__class__.__name__]
        super().__init__(root, bg=config.DEFAULT_BG, **self.dim_dict,
                         **config.FRAME_PADDING)
        self.components = []
        self.grid_kwargs = self.frame_settings["grid_kwargs"]

    def grid(self, **kwargs):
        if len(kwargs) == 0:
            super().grid(**self.grid_kwargs)
        else:
            super().grid(kwargs)


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


class Observer(ABC):
    def __init__(self):
        self.config = MainConfiguration()
        self.theme = Theme()
        self.subject_number = MainConfiguration().SUBJECT_NUMBER
        self.log = dict()
        self.default_keys = ["INFECTED", "SUSCEPTIBLE", "IMMUNE", "ASYMPTOMATIC"]
        self.frames = 0

    @abstractmethod
    def update(self, new_data):
        pass

    def observe(self, observable):
        observable.attach(self)

    def init_log(self):
        self.log = dict(INFECTED=[[0, 0]], SUSCEPTIBLE=[[0, 0]], IMMUNE=[[0, 0]], ASYMPTOMATIC=[[0, 0]])

    def update_logs(self, newdata):
        for k, v in newdata.items():
            if k in self.default_keys:
                self.log[k] = np.concatenate((self.log[k], [[self.frames, len(v)]]), axis=0)
