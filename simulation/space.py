import numpy as np


class Space:
    def __init__(self, denomination, capacity):
        self.id = np.random.randint(low=1e8, high=9.9e8)
        self.denomination = denomination
        self.capacity = capacity
        self.agents_id_list = []
        self.agents_count = 0

    def add_agent(self, agent):
        if self.agents_count < self.capacity:
            self.agents_id_list.append(agent.id)
            agent.spaces_id[self.denomination] = self.id
            self.agents_count = len(self.agents_id_list)
            return True
        return False

    def __repr__(self):
        return f"Space-> denomination: {self.denomination} | " \
               + f"capacity: {self.capacity} | " \
               + f"agents_count: {self.agents_count}"


if __name__ == "__main__":
    pass
