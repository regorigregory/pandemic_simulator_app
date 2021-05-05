from __future__ import annotations
import matplotlib.patches as patches

import numpy as np
from tkinter import Canvas, Tk

from models.ConfigureMe import MainConfiguration, Theme
from models.SubjectContainers import DefaultContainer, CommunitiesContainer
from views.AbstractClasses import ObserverClient, AbstractSimulation
debug = False


class ConcreteSimulation(AbstractSimulation, ObserverClient):

    def __init__(self, root, config=MainConfiguration()):
        super().__init__()
        self.master = root

        self.fig = Canvas(root, width=self.width, height=self.height, bg=self.theme.plot_bg)
        self.fig.grid()
        self.previous_infected = 0

        self.previous_r = 0


    def get_init_func(self):

        if self.config.QUARANTINE_MODE.get():
            ConcreteSimulation.draw_quarantine_boundaries(self.ax)

        if self.config.COMMUNITY_MODE.get():
            ConcreteSimulation.draw_community_boundaries_on_ax(self.ax)
            if debug:
                for center in self._box_of_particles._community_handler.cell_centres:
                    self.ax.text(center[0], center[1], "x", c="green")
        else:
            ConcreteSimulation.draw_main_simulation_canvas_movement_bounds(self.ax)
        self.ax.set_facecolor(Theme().plot_bg)
        self.ax.set_xlim(0, self.width)
        self.ax.set_ylim(0, self.height)

        self._box_of_particles.count_them()
        self.previous_infected = len(self._box_of_particles.counts["INFECTED"]) + len(
            self._box_of_particles.counts["ASYMPTOMATIC"])
        self.previous_r = self.config.SUBJECT_INITIAL_INFECTION_RATIO

        self.notify(self._box_of_particles.counts)
        self.notify({"DAY": 0, "R_RATE": self.previous_r, "R_GROWTH": self.previous_r})

        self.ax.set_xticks([])
        self.ax.set_yticks([])

        # immune
        immune_coords = self.get_current_coordinates(self._box_of_particles.counts["IMMUNE"])

        self.ax.plot(*immune_coords, marker=".",
                     fillstyle="full", linestyle="", color=Theme().immune, markersize=self._marker_radius * 2)

        self.ax.plot(*immune_coords, marker=".",
                     fillstyle="none", linestyle="", color=Theme().immune,
                     markersize=self._infection_zone_radius * 2)

        # susceptible
        susceptible_coords = self.get_current_coordinates(self._box_of_particles.counts["SUSCEPTIBLE"])
        self.ax.plot(*susceptible_coords, marker=".",
                     fillstyle="full", linestyle="", color=Theme().susceptible, markersize=self._marker_radius * 2)

        self.ax.plot(*susceptible_coords, marker=".", fillstyle="none", color=Theme().susceptible, linestyle="",
                     markersize=self._infection_zone_radius * 2)

        # asymptomatic
        asymptomatic_coords = self.get_current_coordinates(self._box_of_particles.counts["ASYMPTOMATIC"])
        self.ax.plot(*asymptomatic_coords, marker=".",
                     fillstyle="full", linestyle="", color=Theme().asymptomatic, markersize=self._marker_radius * 2)

        self.ax.plot(*asymptomatic_coords, marker=".", fillstyle="none", color=Theme().asymptomatic, linestyle="",
                     markersize=self._infection_zone_radius * 2)
        # infected
        infected_coords = self.get_current_coordinates(self._box_of_particles.counts["INFECTED"])

        self.ax.plot(*infected_coords, marker=".",
                     fillstyle="full", linestyle="", color=Theme().infected, markersize=self._marker_radius * 2)

        self.ax.plot(*infected_coords, marker=".", fillstyle="none", color=Theme().infected, linestyle="",
                     markersize=self._infection_zone_radius * 2)

        def func():
            return self.ax.lines

        return func

    def get_animation_function(self):
        frames_per_day = self.config.get_frames_per_day()

        def func(i):
            self.move_guys(i)
            if i % frames_per_day == 0:
                day = i / frames_per_day
                all_infected = len(self._box_of_particles.counts["ASYMPTOMATIC"]) + len(
                    self._box_of_particles.counts["INFECTED"])
                try:
                    r_rate = all_infected/self.previous_infected
                    r_growth = (r_rate - self.previous_r)/self.previous_r

                except ZeroDivisionError:
                    r_rate = 0.0
                    r_growth = 0.0

                self.previous_r = r_rate
                self.previous_infected = all_infected
                r_rate = "{0:.2f}".format(r_rate)
                r_growth = "{0:.2f}%".format(r_growth*100)
                self.notify(
                    {"DAY": int(day), "R_RATE": r_rate, "R_GROWTH": r_growth})

            self.notify(self._box_of_particles.counts)

            infected_coords = self.get_current_coordinates(self._box_of_particles.counts["INFECTED"])
            immune_coords = self.get_current_coordinates(self._box_of_particles.counts["IMMUNE"])
            susceptible_coords = self.get_current_coordinates(self._box_of_particles.counts["SUSCEPTIBLE"])
            asymptomatic_coords = self.get_current_coordinates(self._box_of_particles.counts["ASYMPTOMATIC"])

            self.ax.lines[0].set_data(*immune_coords)
            self.ax.lines[1].set_data(*immune_coords)

            self.ax.lines[2].set_data(*susceptible_coords)
            self.ax.lines[3].set_data(*susceptible_coords)

            self.ax.lines[4].set_data(*asymptomatic_coords)
            self.ax.lines[5].set_data(*asymptomatic_coords)

            self.ax.lines[6].set_data(*infected_coords)
            self.ax.lines[7].set_data(*infected_coords)

            # self._box_of_particles.print_counts()
            return self.ax.lines

        return func

    def start_animation(self):
        pass
        """init_func = self.get_init_func()
        animation_function = self.get_animation_function()
        self.ani = FuncAnimation(self.fig,
                                 animation_function,
                                 init_func=init_func,
                                 interval=1000 / self.config.FRAMES_PER_SECOND,
                                 blit=True)
        return self.ani"""

    def reset(self):
        self._marker_radius = MainConfiguration().SUBJECT_SIZE
        self._infection_zone_radius = MainConfiguration().SUBJECT_INFECTION_RADIUS + MainConfiguration().SUBJECT_SIZE
        self.ani._stop()
        del self.ani
        del self._box_of_particles
        #self.ani = None
        self._box_of_particles = DefaultContainer() if self.config.COMMUNITY_MODE.get() is not True\
            else CommunitiesContainer()
        self.fig.axes[0].clear()
        self.start_animation()
        self.notify(None)
        self.fig.canvas.draw()

    def resume(self):
        self.ani.event_source.start()

    def pause(self):
        self.ani.event_source.stop()

    def draw_subject_with_radius(self, subject: Subject) -> None:
        pass

    @staticmethod
    def draw_community_boundaries_on_ax(ax):
        cells = MainConfiguration().get_community_cells_border_bounds()
        for cell in cells:
            ax.create_rectangle(cell[0][0], cell[1][0], cell[0][1], cell[1][1], outline=Theme().infected, dash=(4, 2))

    @staticmethod
    def draw_quarantine_boundaries(ax):
        q_dims = MainConfiguration().get_quarantine_dimensions()
        inner_padding = MainConfiguration().INNER_PADDING
        ax.create_text(q_dims["x"] + inner_padding, q_dims["y"] + q_dims["height"] - 4 * inner_padding, fill=Theme().infected,
                       font="Courier 14", text="QUARANTINE", angle=90)
        ax.create_rectangle(q_dims["x"], q_dims["y"], q_dims["x"] + q_dims["width"], q_dims["y"] + q_dims["height"],
                            outline=Theme().infected, dash=(4, 2))

    @staticmethod
    def draw_main_simulation_canvas_movement_bounds(ax):
        dims = MainConfiguration().get_particle_movement_border_bounds()
        ax.create_rectangle(dims[0][0], dims[1][0], dims[0][1], dims[1][1], outline=Theme().infected, dash=(4, 2))


if __name__ == "__main__":
    window = Tk()
    window.title("Pandemic Simulator")
    window.configure({"bg": Theme().default_bg})

    MainConfiguration().MAIN_CANVAS_SIZE = [window.winfo_screenwidth(), window.winfo_screenheight()]

    window.geometry(MainConfiguration().get_main_canvas_size_tkinter())
    s = ConcreteSimulation(window)
    ConcreteSimulation.draw_community_boundaries_on_ax(s.fig)
    window.mainloop()
    pass
