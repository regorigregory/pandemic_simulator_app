from Subject import Subject
class NormalSimulation():
    def __init__(self, conf):
        self.subjects = []
        for i in range(0, conf.NUMBER_OF_SUBJECTS):
            self.subjects.append(Subject(conf))