from models.conf import SubjectTypes, Constants
from models.Particle import Particle
from models.Subject import Subject

class Box:
    def __init__(self, config):
        self.contents = []

        if config.SUBJECT_TYPE.value == SubjectTypes.PARTICLE:
            constructor = Particle
        else:
            constructor = Subject

        for i in range(0, config.NUMBER_OF_SUBJECTS.value):
            self.contents.append(constructor(config))
    def move_guys(self):
        for particle in self.contents:
            particle.get_particle_component().update_location()
if __name__ == "__main__":
    box = Box(Constants)