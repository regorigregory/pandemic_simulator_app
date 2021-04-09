from models.conf import Constants
from models.Subject import Subject
from models.MovingParticle import MovingParticle

class BoxOfParticles():
    def __init__(self, cnf):
        self.particles = []
        for i in range(0, cnf.NUMBER_OF_SUBJECTS.value):
            self.particles.append(MovingParticle(cnf))
    def move_guys(self):
        for particle in self.particles:
            particle.update_location()
if __name__ == "__main__":
    box = BoxOfParticles(Constants)