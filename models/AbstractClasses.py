from __future__ import annotations
from abc import ABC, abstractmethod
from models.CollisionHandlers import AxisBased
from models.ConfigureMe import MainConfiguration
from models.Subject import Subject
import numpy as np


class AbstractMovementHandler(ABC):

    def __init__(self):
        self.config = MainConfiguration()
        self.travelling_speed = self.config.QUARANTINE_APPROACHING_SPEED

    def set_direction_to_destination(self, to_be_guided: Subject, coordinate: list[float, float]) -> None:
        particle = to_be_guided.get_particle_component()
        direction_vector = coordinate - particle.position_vector
        direction_vector /= np.sum(direction_vector ** 2) ** 0.5
        particle.velocity_vector = direction_vector * self.travelling_speed

    def _get_box_centre(self, box_bounds: dict[str, float]) -> np.array[float, float]:
        if isinstance(box_bounds, dict):
            return np.array([box_bounds["x"] + box_bounds["width"] / 2,
                      box_bounds["y"] + box_bounds["height"] / 2])
        else:
            width = box_bounds[0][1] - box_bounds[0][0]
            height = box_bounds[1][1] - box_bounds[1][0]

            return np.array([box_bounds[0][0] + width/2,
                             box_bounds[1][0] + height/2])

    @staticmethod
    def calculate_distance(point_from, point_to) -> float:
        return np.sum((point_to - point_from) ** 2) ** 0.5

    @abstractmethod
    def guide_subject_journey(self, to_be_guided: Subject) -> None:
        pass


class AbstractContainerOfSubjects(ABC):
    def __init__(self):
        self.config = MainConfiguration()
        self._infection_handler = AxisBased()
        self.contents = set()
        self._particle_radius = self.config.SUBJECT_SIZE
        self._infection_radius = self.config.SUBJECT_INFECTION_RADIUS + self.config.SUBJECT_SIZE
        self.counts = dict()
        self.count_keys = ["SUSCEPTIBLE", "ASYMPTOMATIC", "INFECTED", "IMMUNE"]
        self.positions_by_status = {v: [] for v in self.count_keys}

        self.init_counts()
        self.r_rate = 0

    @abstractmethod
    def reset(self) -> None:
        pass

    @abstractmethod
    def populate_subjects(self) -> None:
        pass

    @abstractmethod
    def move_guys(self, timestamp: int) -> None:
        pass

    def init_counts(self, exception=None) -> None:
        for k in self.count_keys:
            if exception is None or k not in exception:
                self.counts[k] = set()
        self.positions_by_status = {v: [[], []] for v in self.count_keys}

    def count_them(self, timestamp=0):
        for s in self.contents:
            self.counts[s.get_infection_status(timestamp).name].add(s)

    @staticmethod
    def get_evenly_spaced_specs(bounds: list[list[float, float]], n: int = MainConfiguration().SUBJECT_NUMBER) \
            -> dict[str, float]:
        # thanks to mvw @
        # https://math.stackexchange.com/questions/1039482/how-to-evenly-space-a-number-of-points-in-a-rectangle

        w = bounds[0, 1] - bounds[0, 0]
        h = bounds[1, 1] - bounds[1, 0]
        n_x = ((w / h) * n + (w - h) ** 2 / (4 * (h ** 2))) ** 0.5 - (w - h) / (2 * h)
        n_y = n / n_x
        divisor = (n_y - 1)
        divisor = divisor if (n_y - 1) > 0 else 1
        spacing = h / divisor
        return dict(n_per_column=abs(n_x), n_per_row=abs(n_y), spacing=abs(spacing), w_h_ratio = w/h)

    @staticmethod
    def get_evenly_spaced_coordinates(i: int,
                                      bounds: list[list[float, float]],
                                      n_of_subjects: int = MainConfiguration().SUBJECT_NUMBER) \
            -> list[float, float]:

        dims = AbstractContainerOfSubjects.get_evenly_spaced_specs(bounds, n=n_of_subjects)
        row = int(i / dims["n_per_row"])
        column = i - (row * dims["n_per_row"])

        return [abs(column * dims["spacing"] * dims["w_h_ratio"]) + bounds[0,0], abs(row * dims["spacing"]) + bounds[1,0]]
