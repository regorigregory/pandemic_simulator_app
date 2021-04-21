import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, Animation, TimedAnimation

from models.SubjectContainers import BoxOfSubjects
from matplotlib.widgets import Button
from models.ConfigureMe import Constants
import numpy as np

class AreaChart:
    def __init__(self, config=Constants()):
        super().__init__()
        self.config = config
        self.width, self.height = config.get_dimensions(1, "GRAPH_DIM")
        self.DPI = config.DPI

        self.fig = plt.figure(figsize=(self.width / self.DPI, self.height / self.DPI), dpi=self.DPI)
        self.ax = plt.gca()
        self.frames = 0

        self.log = dict(INFECTED = [[0, 0]], SUSCEPTIBLE = [[0, 0]], IMMUNE = [[0, Constants().NUMBER_OF_SUBJECTS]])

        self.init_graph()
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

    def init_graph(self):
        self.x_data = 0
        self.y_data = 0
        self.plot = plt.stackplot([], [], [], [], colors = ["#4A306D", "#0E273C"])
        self.ax.set_facecolor("#D3BCCC")
        self.ax.set_ylim(0, Constants().NUMBER_OF_SUBJECTS)
        self.ax.set_xticks([])
        self.ax.set_yticks([])

    def update_logs(self, newdata):
        for k, v in newdata.items():
            if(k == "IMMUNE"):
                self.log[k] = np.concatenate((self.log[k], [[self.frames, Constants().NUMBER_OF_SUBJECTS - len(v)]]), axis = 0)

            else:
                self.log[k] = np.concatenate((self.log[k], [[self.frames, len(v)]]), axis = 0)

    def update(self, new_data):
        self.frames += 1
        self.update_logs(new_data)
        self.ax.set_xlim(0, self.frames)

        self.redraw_verts()
        # to be continued tomorrow

    def redraw_verts(self):
        self.plot[0].set_verts([np.concatenate([self.log["INFECTED"], [[self.frames, 0]]])],
                               closed = True)
        self.plot[1].set_verts([np.concatenate([self.log["IMMUNE"], [[self.frames, Constants().NUMBER_OF_SUBJECTS]]])],
                               closed = True)
        self.fig.canvas.draw()

    def observe(self, observable):
        observable.attach(self)



if __name__ == "__main__":
    import matplotlib.pyplot as plt

    plt.ioff()
    fig = plt.Figure()
    ax = plt.gca()
    filled = ax.stackplot(range(0,10),  np.random.randint(0,10, 10), np.random.randint(0,10, 10))
    plt.show()
