from models.Subject import Subject
from typing import List
from models.conf import InfectionStatuses
class Naive(object):
    def __init__(self):
        self.init_counts()

    def init_counts(self):
        self.counts = dict(
            SUSCEPTIBLE=set(),
            INFECTED=set(),
            IMMUNE=set()
        )
    def handle_infections(self, timestamp: int, a_subject: Subject, subjects: List[Subject]):

        self.init_counts()
        if(a_subject.get_infection_status(timestamp) != InfectionStatuses.IMMUNE):

            for other in subjects:
                if(other.get_infection_status(timestamp) != InfectionStatuses.IMMUNE):
                    if (a_subject != other and a_subject.are_we_too_close(other)):
                        a_subject.encounter_with(timestamp, other)
                new_status = other.get_infection_status(timestamp)
                if new_status == InfectionStatuses.INFECTED:
                    self.counts["INFECTED"].add(other)
                    if(other in self.counts["SUSCEPTIBLE"]):
                        self.counts["SUSCEPTIBLE"].remove(other)
                    else:
                        self.counts[new_status.name].add(other)
        else:
            self.counts["IMMUNE"].add(a_subject)

    def print_counts(self):
        import sys
        sys.stdout.write("\nInfected: {}, Immune: {}, Susceptible: {}".format(
            len(self.counts["INFECTED"]),
            len(self.counts["IMMUNE"]),
            len(self.counts["SUSCEPTIBLE"])

        ))

if __name__ == "__main__":
    testObject = Naive()