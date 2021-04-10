from models.conf import SubjectTypes, Constants
from models.Particle import Particle
from models.Subject import Subject
from models.InfectionHandlers import Naive
class Box:
    def __init__(self, config):
        self.contents = []

        if config.SUBJECT_TYPE.value == SubjectTypes.PARTICLE:
            constructor = Particle
        else:
            constructor = Subject

        for i in range(0, config.NUMBER_OF_SUBJECTS.value):
            self.contents.append(constructor(config))
    def move_guys(self, timestamp, infection_handler: Naive = None):
        for particle in self.contents:
            particle.get_particle_component().update_location()
            if (infection_handler is not None):
                infection_handler.handle_infections(timestamp, particle, self.contents)
if __name__ == "__main__":
    box = Box(Constants)