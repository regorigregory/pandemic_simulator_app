from models.ConfigureMe import MainConfiguration, Theme
import numpy as np


class AreaChart:
    def __init__(self):
        self.config = MainConfiguration()
        self.theme = Theme()
        self.width, self.height = self.config.get_dimensions("GRAPH_DIM")
        self.DPI = self.config.DPI

        self.fig = plt.figure(figsize=(self.width / self.DPI, self.height / self.DPI), dpi=self.DPI)
        self.ax = self.fig.add_subplot()
        self.frames = 0


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
        self.log = dict(INFECTED = [[0, 0]], SUSCEPTIBLE = [[0, 0]], IMMUNE = [[0, MainConfiguration().SUBJECT_NUMBER]])
        self.x_data = 0
        self.y_data = 0
        self.plot = plt.stackplot([], [], [], [], colors = self.theme.area_plot_colours)
        self.ax.set_facecolor(self.theme.area_plot_bg)
        self.ax.set_ylim(0, MainConfiguration().SUBJECT_NUMBER)
        self.ax.set_xlim(0, self.frames + 1)
        self.ax.set_xticks([])
        self.ax.set_yticks([])

    def update_logs(self, newdata):
        for k, v in newdata.items():
            if(k == "IMMUNE"):
                self.log[k] = np.concatenate((self.log[k], [[self.frames, MainConfiguration().SUBJECT_NUMBER - len(v)]]), axis = 0)

            else:
                self.log[k] = np.concatenate((self.log[k], [[self.frames, len(v)]]), axis = 0)

    def update(self, new_data):
        if not new_data:
            self.frames = 0
            self.init_graph()
            self.redraw_verts()
            self.fig.canvas.draw()

        else:

            self.frames += 1
            self.update_logs(new_data)
            self.ax.set_xlim(0, self.frames)
            self.redraw_verts()
            # to be continued tomorrow

    def redraw_verts(self):
        self.plot[0].update({"verts": [np.concatenate([self.log["INFECTED"], [[self.frames, 0]]])]})
        self.plot[1].update({"verts": [np.concatenate([self.log["IMMUNE"], [[self.frames, MainConfiguration().SUBJECT_NUMBER]]])],
                             })
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
