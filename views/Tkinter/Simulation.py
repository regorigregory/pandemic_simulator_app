from __future__ import annotations
import matplotlib.patches as patches

import numpy as np
from tkinter import Canvas, Tk

from models.ConfigureMe import MainConfiguration, Theme
from models.SubjectContainers import DefaultContainer, CommunitiesContainer
from models.Subject import Subject
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
        self.circles = dict()

    def draw_subject_with_radius(self, subject: Subject) -> None:
        sid = subject.id
        particle_position = subject.get_particle_component().position_vector
        infection_status = subject.get_infection_status(0).name
        current_colour = getattr(Theme(), infection_status.lower())

        core_radius = self.config.SUBJECT_SIZE
        infection_radius = self.config.SUBJECT_INFECTION_RADIUS

        o1 = self.fig.create_oval((particle_position-core_radius).tolist(),
                                (particle_position+core_radius).tolist(),
                                fill=current_colour,
                                outline = current_colour)
        o2 = self.fig.create_oval((particle_position-core_radius-infection_radius).tolist(),
                                (particle_position+core_radius+infection_radius).tolist(),
                                outline=current_colour)
        self.circles[sid] = [o1, o2]
        pass

    def update_subject_location_on_canvas(self, subject):
        subject_location = subject.get_particle_component().position_vector
        self.fig.move(self.circles[subject.id][0], *subject_location.tolist())
        self.fig.move(self.circles[subject.id][1], *subject_location.tolist())
        self.fig.update()


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




if __name__ == "__main__":
    window = Tk()
    window.title("Pandemic Simulator")
    window.configure({"bg": Theme().default_bg})

    MainConfiguration().MAIN_CANVAS_SIZE = [window.winfo_screenwidth(), window.winfo_screenheight()]

    window.geometry(MainConfiguration().get_main_canvas_size_tkinter())
    sim = ConcreteSimulation(window)
    sub = Subject()
    print(sub.get_particle_component().position_vector)
    sub.get_particle_component().update_location(10)
    print(sub.get_particle_component().position_vector)

    sim.draw_subject_with_radius(sub)
    ConcreteSimulation.draw_community_boundaries_on_ax(sim.fig)
    window.after(1, sim.update_subject_location_on_canvas(sub))

    window.mainloop()
    pass
