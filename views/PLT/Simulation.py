from __future__ import annotations
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, Animation, TimedAnimation
from abc import ABC, abstractmethod
from models.SubjectContainers import DefaultContainer, CommunitiesContainer
from matplotlib import patches
from models.ConfigureMe import MainConfiguration, Theme
import numpy as np
debug = True

class AbstractSimulation(ABC):
    @abstractmethod
    def resume(self):
        pass
    def pause(self):
        pass
    def start_animation(self):
        pass
    def reset(self):
        pass


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


class ConcreteSimulation(ObserverClient, AbstractSimulation):

    def __init__(self, config=MainConfiguration(), container=None):
        super().__init__()
        self.config = config
        self.width, self.height = config.get_dimensions("SimulationFrame")
        self.DPI = config.DPI
        self._marker_radius = config.SUBJECT_SIZE
        self._infection_zone_radius = config.SUBJECT_INFECTION_RADIUS + config.SUBJECT_SIZE

        self._box_of_particles = CommunitiesContainer() if self.config.COMMUNITY_MODE.get() else ContainerOfSubjects()
        self._infection_handler = self._box_of_particles._infection_handler
        self._communities_handler = None

        self.fig = plt.figure(figsize=(self.width / self.DPI, self.height / self.DPI), dpi=self.DPI)
        self.ax = self.fig.add_subplot()


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

        if self.config.QUARANTINE_MODE.get():
            ConcreteSimulation.draw_quarantine_boundaries(self.ax)

        if self.config.COMMUNITY_MODE.get():
            ConcreteSimulation.draw_community_boundaries_on_ax(self.ax)
            if debug:
                for center in self._box_of_particles._community_handler.cell_centres:
                    self.ax.text(center[0], center[1],"x", c="green")

        self.ax.set_facecolor(Theme().plot_bg)
        self.ax.set_xlim(0, self.width)
        self.ax.set_ylim(0, self.height)

        self.notify(self._infection_handler.counts)

        self.ax.set_xticks([])
        self.ax.set_yticks([])

        # immune
        IMMUNE_COORDS = self.get_current_coordinates(self._infection_handler.counts["IMMUNE"])

        self.ax.plot(*IMMUNE_COORDS,  marker=".",
                     fillstyle="full", linestyle="", color=Theme().immune, markersize=self._marker_radius * 2)

        self.ax.plot(*IMMUNE_COORDS, marker=".",
                     fillstyle="none", linestyle="", color=Theme().immune,
                     markersize= self._infection_zone_radius * 2)

        # susceptible
        SUSCEPTIBLE_COORDS = self.get_current_coordinates(self._infection_handler.counts["SUSCEPTIBLE"])
        self.ax.plot(*SUSCEPTIBLE_COORDS, marker=".",
                     fillstyle="full", linestyle="", color=Theme().susceptible, markersize=self._marker_radius * 2)

        self.ax.plot(*SUSCEPTIBLE_COORDS, marker=".", fillstyle="none", color=Theme().susceptible, linestyle="",
                     markersize= self._infection_zone_radius * 2)

        # asymptomatic
        ASYMPTOMATIC_COORDS = self.get_current_coordinates(self._infection_handler.counts["ASYMPTOMATIC"])
        self.ax.plot(*ASYMPTOMATIC_COORDS, marker=".",
                     fillstyle="full", linestyle="", color=Theme().asymptomatic, markersize=self._marker_radius * 2)

        self.ax.plot(*ASYMPTOMATIC_COORDS, marker=".", fillstyle="none", color=Theme().asymptomatic, linestyle="",
                     markersize=self._infection_zone_radius * 2)
        # infected
        INFECTED_COORDS = self.get_current_coordinates(self._infection_handler.counts["INFECTED"])

        self.ax.plot(*INFECTED_COORDS, marker=".",
                     fillstyle="full", linestyle="", color=Theme().infected, markersize=self._marker_radius * 2)

        self.ax.plot(*INFECTED_COORDS, marker=".", fillstyle="none", color=Theme().infected, linestyle="",
                     markersize=self._infection_zone_radius * 2)

        # adding quarantine bounding box



        def func():
            return self.ax.lines

        return func

    def get_animation_function(self):
        def func(i):
            self.move_guys(i)

            self.notify(self._infection_handler.counts)

            INFECTED_COORDS = self.get_current_coordinates(self._infection_handler.counts["INFECTED"])
            IMMUNE_COORDS = self.get_current_coordinates(self._infection_handler.counts["IMMUNE"])
            SUSCEPTIBLE_COORDS = self.get_current_coordinates(self._infection_handler.counts["SUSCEPTIBLE"])
            ASYMPTOMATIC_COORDS = self.get_current_coordinates(self._infection_handler.counts["ASYMPTOMATIC"])

            self.ax.lines[0].set_data(*IMMUNE_COORDS)
            self.ax.lines[1].set_data(*IMMUNE_COORDS)

            self.ax.lines[2].set_data(*SUSCEPTIBLE_COORDS)
            self.ax.lines[3].set_data(*SUSCEPTIBLE_COORDS)

            self.ax.lines[4].set_data(*ASYMPTOMATIC_COORDS)
            self.ax.lines[5].set_data(*ASYMPTOMATIC_COORDS)

            self.ax.lines[6].set_data(*INFECTED_COORDS)
            self.ax.lines[7].set_data(*INFECTED_COORDS)

            # self._infection_handler.print_counts()
            return self.ax.lines

        return func

    def start_animation(self):
        init_func = self.get_init_func()
        animation_function = self.get_animation_function()
        self.ani = FuncAnimation(self.fig,
                             animation_function,
                             init_func=init_func,
                             interval=1000/(MainConfiguration().DAYS_PER_SECOND * MainConfiguration().FRAME_MULTIPLIER),
                             blit = True)
        return self.ani

    def reset(self):
        self._marker_radius = MainConfiguration().SUBJECT_SIZE
        self._infection_zone_radius = MainConfiguration().SUBJECT_INFECTION_RADIUS + MainConfiguration().SUBJECT_SIZE
        self.ani._stop()
        self.ani = None
        self._box_of_particles = DefaultContainer() if self.config.COMMUNITY_MODE.get() != True else CommunitiesContainer()
        self._infection_handler = self._box_of_particles._infection_handler
        self.fig.axes[0].clear()
        self.start_animation()
        self.notify(None)
        self.fig.canvas.draw()


    def resume(self):
        self.ani.event_source.start()

    def pause(self):
        self.ani.event_source.stop()

    @staticmethod
    def draw_community_boundaries_on_ax(ax) -> list[[float, float], [float, float]]:
        config = MainConfiguration()
        main_dimensions = config.get_particle_position_boundaries()
        full_width = main_dimensions[0][1] - main_dimensions[0][0]
        x_start = main_dimensions[0][0]

        full_height = main_dimensions[1][1]
        padding = config.INNER_PADDING
        rows = config.COMMUNITIES_ROWS
        columns = config.COMMUNITIES_COLUMNS
        row_height = full_height / rows - padding
        column_width = full_width / columns - padding
        patch_dimensions = dict(width=column_width - padding, height=row_height - padding)

        cells = []
        for row in range(rows):
            for column in range(columns):
                x = x_start + padding + column * column_width
                y = padding + row * row_height
                width = patch_dimensions["width"]
                height = patch_dimensions["height"]
                ax.add_patch(patches.Rectangle([x, y],
                             width,
                             height,
                             facecolor="none",
                             linewidth=1,
                             edgecolor=Theme().infected,
                             linestyle="--"
                             ))
                if debug:
                    ax.text(x, y, "P({:.0f}, {:.0f})".format(x, y), c = "green")

                cells.append([[x, x + width], [y, y + height]])
        return cells

    @staticmethod
    def draw_quarantine_boundaries(ax):
        if MainConfiguration().QUARANTINE_MODE.get():
            q_dims = MainConfiguration().get_quarantine_dimensions()
            ax.text(q_dims["x"],
                         q_dims["height"] - q_dims["y"],
                         "QUARANTINE", color = Theme().infected,
                         fontsize = "large")
            ax.add_patch(patches.Rectangle([q_dims["x"], q_dims["y"]], q_dims["width"], q_dims["height"],
                                                facecolor = "none",
                                                linewidth = 1,
                                                edgecolor = Theme().infected,
                                                linestyle = "--"))
if __name__ == "__main__":
    import matplotlib.pyplot as plt

    plt.ioff()
    ViewBox = ConcreteSimulation(container=DefaultContainer())
    a = ViewBox.start_animation()
    a.event_source.stop()
    plt.show()
    """init_func = ViewBox.get_init_func()
    animation_function = ViewBox.get_animation_function()

    anim = FuncAnimation(ViewBox.fig,
                         animation_function,
                         init_func = init_func,
                         interval=20)"""
