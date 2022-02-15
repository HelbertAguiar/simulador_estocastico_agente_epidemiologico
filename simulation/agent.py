from names import get_first_name, get_last_name
import numpy as np


class Agent:
    def __init__(self, identification: int, status: int = None):
        self.id = identification
        self.status = status or 0
        self.status_age = 0
        # self.name = self._random_name_generator(identification)
        self.risk_factor = min(np.random.chisquare(3.5) / 15, 1.0)
        self.spaces_id = {"house": None, "work": None, "night": None}

    @staticmethod
    def _random_name_generator(agent_id):
        return f"{get_first_name()}{get_last_name()}#{agent_id}"

    def infect(self, incubation_phase=True):
        self.status = 1 if incubation_phase else 2
        self.status_age = 0

    def __repr__(self):
        return f"Agent {self.name} - Status: {self.status} (For {self.status_age} days)"


if __name__ == "__main__":
    pass
