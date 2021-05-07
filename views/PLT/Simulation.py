from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib.animation import FuncAnimation

from models.ConfigureMe import MainConfiguration, Theme
from models.SubjectContainers import DefaultContainer, CommunitiesContainer
from views.AbstractClasses import ObserverClient, AbstractSimulation
debug = False


class ConcreteSimulation(AbstractSimulation, ObserverClient):

    def __init__(self):
        super().__init__()
        plt.ioff()
        self.DPI = self.config.DPI
        self.ani = None
        self.fig = plt.figure(figsize=(self.width / self.DPI, self.height / self.DPI), dpi=self.DPI)
        self.fig.subplots_adjust(left=0, bottom=0.05, right=0.95, top=1, wspace=0, hspace=0)
        self.fig.patch.set_facecolor(Theme().default_bg)
        self.ax = self.fig.add_subplot()
        for spine in self.ax.spines.values():
            spine.set_visible(False)
        self.days = 0
        self.ax.set_facecolor(Theme().plot_bg)
        self.fig.set_edgecolor(Theme().plot_bg)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.last_core_radius = MainConfiguration().SUBJECT_SIZE * 2
        self.last_infection_radius = (MainConfiguration().SUBJECT_INFECTION_RADIUS + MainConfiguration().SUBJECT_SIZE) * 2

        ConcreteSimulation.draw_main_simulation_canvas_movement_bounds(self.ax)

    def get_init_func(self):
        self.days = 0

        if self.config.QUARANTINE_MODE.get():
            ConcreteSimulation.draw_quarantine_boundaries(self.ax)

        if self.config.COMMUNITY_MODE.get():
            ConcreteSimulation.draw_community_boundaries_on_ax(self.ax)
            if debug:
                for center in self._box_of_particles._community_handler.cell_centres:
                    self.ax.text(center[0], center[1], "x", c="green")
        else:
            ConcreteSimulation.draw_main_simulation_canvas_movement_bounds(self.ax)

        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_xlim(0, self.width)
        self.ax.set_ylim(0, self.height)
        #self.ax.axis('off')

        self._box_of_particles.count_them()

        self.previous_infected = len(self._box_of_particles.counts["INFECTED"]) + len(
            self._box_of_particles.counts["ASYMPTOMATIC"])
        self.previous_r = 1

        self.notify(self._box_of_particles.counts)
        self.notify({"DAY": 0, "R_RATE": "{:.2f}".format(self.previous_r), "R_GROWTH": "0.0%"})

        self.ax.plot([], marker=".",
                     fillstyle="full", linestyle="", color=Theme().immune, markersize=self.last_core_radius)

        self.ax.plot([], marker=".",
                     fillstyle="none", linestyle="", color=Theme().immune,
                     markersize=self.last_infection_radius)

        # susceptible
        self.ax.plot([], marker=".",
                     fillstyle="full", linestyle="", color=Theme().susceptible, markersize=self.last_core_radius)

        self.ax.plot([], marker=".", fillstyle="none", color=Theme().susceptible, linestyle="",
                     markersize=self.last_infection_radius)

        # asymptomatic
        self.ax.plot([], marker=".",
                     fillstyle="full", linestyle="", color=Theme().asymptomatic, markersize=self.last_core_radius)

        self.ax.plot([], marker=".", fillstyle="none", color=Theme().asymptomatic, linestyle="",
                     markersize=self.last_infection_radius)
        # infected

        self.ax.plot([], marker=".",
                     fillstyle="full", linestyle="", color=Theme().infected, markersize=self.last_core_radius)

        self.ax.plot([], marker=".", fillstyle="none", color=Theme().infected, linestyle="",
                     markersize=self.last_infection_radius)

        def func():
            return self.ax.lines

        return func

    def get_animation_function(self):

        def func(i):
            frames_per_day = self.config.get_frames_per_day()

            self.move_guys(i)
            if i % frames_per_day == 0 and i != 0:
                self.days += 1

                r_rate = self._box_of_particles.r_rate
                try:
                    r_growth = (r_rate - self.previous_r)/self.previous_r
                except ZeroDivisionError:
                    r_growth = 0
                self.previous_r = r_rate
                r_rate = "{0:.2f}".format(r_rate)
                r_growth = "{0:.2f}%".format(r_growth*100)
                self.notify(
                    {"DAY": int(self.days), "R_RATE": r_rate, "R_GROWTH": r_growth})

            self.notify(self._box_of_particles.counts)

            """infected_coords = np.swapaxes(self._box_of_particles.positions_by_status["INFECTED"], 0, 1).astype(int)
            immune_coords = np.swapaxes(self._box_of_particles.positions_by_status["IMMUNE"], 0, 1).astype(int)
            susceptible_coords = np.swapaxes(self._box_of_particles.positions_by_status["SUSCEPTIBLE"], 0, 1).astype(int)
            asymptomatic_coords = np.swapaxes(self._box_of_particles.positions_by_status["ASYMPTOMATIC"], 0, 1).astype(int)
            """
            infected_coords = self.get_current_coordinates_by_key("INFECTED")
            immune_coords = self.get_current_coordinates_by_key("IMMUNE")
            susceptible_coords = self.get_current_coordinates_by_key("SUSCEPTIBLE")
            asymptomatic_coords = self.get_current_coordinates_by_key("ASYMPTOMATIC")

            self.ax.lines[0].set_data(*immune_coords)
            self.ax.lines[1].set_data(*immune_coords)


            self.ax.lines[2].set_data(*susceptible_coords)
            self.ax.lines[3].set_data(*susceptible_coords)

            self.ax.lines[4].set_data(*asymptomatic_coords)
            self.ax.lines[5].set_data(*asymptomatic_coords)

            self.ax.lines[6].set_data(*infected_coords)
            self.ax.lines[7].set_data(*infected_coords)
            core_radius = MainConfiguration().SUBJECT_SIZE * 2
            infection_radius = (MainConfiguration().SUBJECT_INFECTION_RADIUS + MainConfiguration().SUBJECT_SIZE) * 2

            if core_radius != self.last_core_radius or infection_radius != self.last_infection_radius:
                self.last_core_radius = core_radius
                self.last_infection_radius = infection_radius
                self.ax.lines[0].set_markersize(core_radius)
                self.ax.lines[1].set_markersize(infection_radius)

                self.ax.lines[0].set_markersize(core_radius)
                self.ax.lines[1].set_markersize(infection_radius)

                self.ax.lines[2].set_markersize(core_radius)
                self.ax.lines[3].set_markersize(infection_radius)

                self.ax.lines[4].set_markersize(core_radius)
                self.ax.lines[5].set_markersize(infection_radius)
                self.ax.lines[6].set_markersize(core_radius)
                self.ax.lines[7].set_markersize(infection_radius)
            # self._box_of_particles    .print_counts()"""
            return self.ax.lines

        return func

    def start(self):
        init_func = self.get_init_func()
        animation_function = self.get_animation_function()
        self.ani = FuncAnimation(self.fig,
                                 animation_function,
                                 init_func=init_func,
                                 interval=1000 / self.config.FRAMES_PER_SECOND,
                                 blit=True)
        return self.ani

    def reset(self):
        self._marker_radius = MainConfiguration().SUBJECT_SIZE
        self._infection_zone_radius = MainConfiguration().SUBJECT_INFECTION_RADIUS + MainConfiguration().SUBJECT_SIZE
        self.pause()
        if self.ani is not None:
            self.ani._stop()
            self.ani = None
        del self._box_of_particles
        #self.ani = None
        self._box_of_particles = DefaultContainer() if self.config.COMMUNITY_MODE.get() is not True\
            else CommunitiesContainer()
        for x in self.fig.axes:
            x.clear()
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        #self.start()
        self.notify(None)
        self.fig.canvas.draw()

    def resume(self):
        if self.ani is not None:
            self.ani.event_source.start()

    def pause(self):
        if self.ani is not None:
            self.ani.event_source.stop()

    @staticmethod
    def draw_community_boundaries_on_ax(ax):
        cells = MainConfiguration().get_community_cells_border_bounds()
        for cell in cells:
            x = cell[0][0]
            y = cell[1][0]
            width = cell[0][1] - x
            height = cell[1][1] - y
            ax.add_patch(patches.Rectangle((x, y),
                                           width,
                                           height,
                                           facecolor="none",
                                           linewidth=1,
                                           edgecolor=Theme().infected,
                                           linestyle="--"
                                           ))
            if debug:
                ax.text(x, y, "P({:.0f}, {:.0f})".format(x, y), c="green")

    @staticmethod
    def draw_quarantine_boundaries(ax):
        if MainConfiguration().QUARANTINE_MODE.get():
            q_dims = MainConfiguration().get_quarantine_dimensions()
            inner_padding = MainConfiguration().INNER_PADDING
            ax.text(q_dims["x"] + inner_padding,
                    q_dims["y"] + inner_padding,
                    "QUARANTINE",
                    color=Theme().infected,
                    fontsize="large",
                    rotation=90)
            ax.add_patch(patches.Rectangle((q_dims["x"], q_dims["y"]), q_dims["width"], q_dims["height"],
                                           facecolor="none",
                                           linewidth=1,
                                           edgecolor=Theme().infected,
                                           linestyle="--"))

    @staticmethod
    def draw_main_simulation_canvas_movement_bounds(ax):
        q_dims = MainConfiguration().get_particle_movement_border_bounds()
        ax.add_patch(
            patches.Rectangle((q_dims[0, 0], q_dims[1, 0]),
                              q_dims[0, 1] - q_dims[0, 0],
                              q_dims[1, 1] - q_dims[1, 0],
                              facecolor="none",
                              linewidth=1,
                              edgecolor=Theme().infected,
                              linestyle="--"))


if __name__ == "__main__":
    pass
