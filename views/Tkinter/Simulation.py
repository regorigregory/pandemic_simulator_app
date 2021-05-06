from __future__ import annotations
import matplotlib.patches as patches
import time
import numpy as np
from tkinter import Canvas, Tk

from models.ConfigureMe import MainConfiguration, Theme
from models.SubjectContainers import DefaultContainer, CommunitiesContainer
from models.Subject import Subject
from views.AbstractClasses import ObserverClient, AbstractSimulation
from views.TkinterPLTFrames import SimulationFrame

debug = False


class ConcreteSimulation(AbstractSimulation, ObserverClient):

    def __init__(self, root):
        super().__init__()
        self.master = root

        self.canvas = Canvas(root, width=self.width, height=self.height, bg=self.theme.plot_bg)
        print("Canvas size: {}, {}".format(self.width, self.height))
        self.canvas.grid()
        self.previous_infected = 0

        self.previous_r = 0
        self.circles = dict()
        self.init_simulation()


    def init_simulation(self):
        if self.config.QUARANTINE_MODE:
            ConcreteSimulation.draw_quarantine_boundaries(self.canvas)

        if self.config.COMMUNITY_MODE:
            ConcreteSimulation.draw_community_boundaries_on_ax(self.canvas)
        else:
            ConcreteSimulation.draw_main_simulation_canvas_movement_bounds(self.canvas)
        for s in self._box_of_particles.contents:
            self.draw_subject_with_radius(s)

    def draw_subject_with_radius(self, subject: Subject) -> None:
        sid = subject.id
        particle_position = subject.get_particle_component().position_vector.astype(int)
        infection_status = subject.get_infection_status(0).name
        current_colour = getattr(Theme(), infection_status.lower())

        core_radius = self.config.SUBJECT_SIZE
        infection_radius = self.config.SUBJECT_INFECTION_RADIUS
        core_ellipse_bounds = [(particle_position + core_radius).tolist(), (particle_position - core_radius ).tolist()]
        infection_ellipse_bounds = [(particle_position - core_radius - infection_radius).tolist(),
                                    (particle_position + core_radius + infection_radius).tolist()]

        o1 = self.canvas.create_oval(*core_ellipse_bounds,
                                     fill=current_colour,
                                     outline = current_colour)
        o2 = self.canvas.create_oval(*infection_ellipse_bounds,
                                     outline=current_colour)


        self.circles[sid] = [o1, o2]
        pass

    def update_subject_location_on_canvas(self, subject, frame):

        old_position = subject.get_particle_component().position_vector
        subject.get_particle_component().update_location(frame)
        delta_position = subject.get_particle_component().position_vector - old_position
        print("{}, {}".format(*delta_position))
        self.canvas.move(self.circles[subject.id][0], *delta_position.tolist())
        self.canvas.move(self.circles[subject.id][1], *delta_position.tolist())

    def start(self):
        frame = 0
        while True:
            frame += 1

            #time.sleep(0.001)
            for s in self._box_of_particles.contents:
                self.update_subject_location_on_canvas(s, frame)
            self.canvas.update()

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
        ax.create_text(dims[0][1]-20, dims[1][1]-20,
                                       fill=Theme().infected,
                                       font="Courier 8", text="({:.2f},{:.2f})".format(dims[0][1], dims[1][1]))
    def reset(self):
        self._marker_radius = MainConfiguration().SUBJECT_SIZE
        self._infection_zone_radius = MainConfiguration().SUBJECT_INFECTION_RADIUS + MainConfiguration().SUBJECT_SIZE
        self.ani._stop()
        del self.ani
        del self._box_of_particles
        #self.ani = None
        self._box_of_particles = DefaultContainer() if self.config.COMMUNITY_MODE.get() is not True\
            else CommunitiesContainer()
        self.canvas.axes[0].clear()
        self.start()
        self.notify(None)
        self.canvas.canvas.draw()

    def resume(self):
        self.ani.event_source.start()

    def pause(self):
        self.ani.event_source.stop()

if __name__ == "__main__":
    import ctypes

    window = Tk()
    window.title("Pandemic Simulator")
    window.configure({"bg": Theme().default_bg})
    MainConfiguration().MAIN_CANVAS_SIZE = [window.winfo_screenwidth(), window.winfo_screenheight()]

    window.geometry(MainConfiguration().get_main_canvas_size_tkinter())

    sim = ConcreteSimulation(window)
    window.after(0, sim.start())
    window.mainloop()
    pass
