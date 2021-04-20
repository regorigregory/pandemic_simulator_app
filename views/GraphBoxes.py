import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, Animation, TimedAnimation

from models.SubjectContainers import BoxOfSubjects
from matplotlib.widgets import Button
from models.ConfigureMe import Constants
import numpy as np


class PLTGraph:
    def __init__(self, config=Constants()):
        self.config = config
        self.width, self.height = config.get_dimensions(1, "GRAPH_DIM")
        self.DPI = config.DPI

        self.fig = plt.figure(figsize=(self.width / self.DPI, self.height / self.DPI), dpi=self.DPI)
        self.ax = plt.gca()
        self.frames = 0
        self.frame_data = dict(INFECTED = [], IMMUNE = [], SUSCEPTIBLE = [])

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
    def init(self):
        self.x_data = 0
        self.y_data = 0
        self.plot = plt.stackplot([], [], [], [])
        self.ax.set_yim(0, Constants().NUMBER_OF_SUBJECTS)
        pass

    def update(self, new_data):
        self.frames += 1
        infected = np.empty([0, 2])

        infected = np.concatenate((infected, [0, 0]))
        susceptible = np.concatenate((infected, [0, 0]))
        i = 1
        for k,v in new_data.items():
            infected = np.concatenate((infected, [i, self.frame_data[k][i]]))
            susceptible = np.concatenate(
                (susceptible, [i, self.frame_data["INFECTED"][i] + self.frame_data["SUSCEPTIBLE"][i]]))
        infected = np.concatenate((infected, [i, 0]))
        susceptible = np.concatenate((susceptible, [i, 0]))
        self.redraw_graps()
        # to be continued tomorrow

    def redraw_verts(self):
        infected = np.empty([0,2])

        infected = np.concatenate((infected, [0,0]))
        susceptible = np.concatenate((infected, [0,0]))

        for i in range(self.frames):
            infected = np.concatenate((infected, [i, self.frame_data["INFECTED"][i]]))
            susceptible = np.concatenate((susceptible, [i, self.frame_data["INFECTED"][i] + self.frame_data["SUSCEPTIBLE"][i]]))
        infected = np.concatenate((infected, [i, 0]))
        susceptible = np.concatenate((susceptible, [i,0]))

        self.plot[0].set_verts([infected], True)
        self.plot[1].set_verts([susceptible], True)
        plt.redraw()

    def observe(self, observable):
        observable.attach(self)



if __name__ == "__main__":
    import matplotlib.pyplot as plt

    plt.ioff()
    fig = plt.Figure()
    ax = plt.gca()
    filled = ax.stackplot(range(0,10),  np.random.randint(0,10, 10), np.random.randint(0,10, 10))
    plt.show()
