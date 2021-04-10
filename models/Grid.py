from models.Particle import Particle
from models.conf import Constants
class GridCell():
    def __init__(self, x,y,u,v):
        self.x = x
        self.y = y
        self.u = u
        self.v = v
        self.particles: set[Particle] = set()

    def add(self, particle: Particle)->None:
        self.particles.add(particle)

    def remove(self, particle: Particle)->None:
        if self.particles.__contains__(particle):
            self.particles.remove(particle)
    def contains_particle(self, particle: Particle)->bool:
        return self.particles.__contains__(particle)
    def has_particles(self):
        return len(self.particles) > 0
class Grid():
    def __init__(self, conf: Constants):
        self.virtual_radius = conf.INFECTION_RADIUS.value + conf.PARTICLE_RADIUS.value
        self.real_radius = conf.PARTICLE_RADIUS.value
        self.grid_dimensions = conf.DIMENSIONS.value

        self.grid_cell_size = self._calculate_cell_size()
        self.cells = self._populate_cells()
        self.colliding_cells = set()
    def _populate_cells(self):
        pass
    def _calculate_cell_size(self):
        pass
    def update_particles_locations(self):
        self.colliding_cells = set()
        #check collisions here
        #stop at collision point -> or more accurately, move them back
        #add to colliding cells for quick view update
        #change direction to opposite of the collision vectors
        #change velocity vector direction the same way
        pass
if __name__ == "__main__":
    x = GridCell(0,0,10,10)