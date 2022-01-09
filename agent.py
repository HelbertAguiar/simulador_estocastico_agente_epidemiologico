import numpy as np
from names import get_first_name, get_last_name
from collections import Counter
from random import random, sample


COVID_STAGES = {0: "healthy", 1: "incubating", 2: "infected",
                3: "healed/immune", 4: "deceased"}
IMMUNE_STATUS = [1, 2, 3, 4]


class Agent:
    def __init__(self, identification, status=None):
        self.id = identification
        self.status = status or 0
        self.status_age = 0
        self.name = self._random_name_generator(identification)
        self.spaces_id = {"house": None, "work": None, "night": None}

    @staticmethod
    def _random_name_generator(agent_id):
        return f"{get_first_name()}{get_last_name()}#{agent_id}"

    def infect(self):
        self.status = 1
        self.status_age = 0

    def __repr__(self):
        return f"Agent {self.name} - Status: {self.status} (For {self.status_age} days)"


class Space:
    def __init__(self, denomination, capacity):
        self.id = np.random.randint(low=1e12, high=9.9e12)
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


class Environment:
    def __init__(self, max_agents, max_house_spaces, max_work_spaces, max_night_spaces,
                 max_agents_in_house=5, max_agents_in_work=10, max_agents_in_night=10):
        self.is_populated = False
        self.starting_agents = max_agents
        self.agents = []
        self.house_spaces = self._build_spaces("house", max_agents_in_house,
                                               max_house_spaces)
        self.work_spaces = self._build_spaces("work", max_agents_in_work, max_work_spaces)
        self.night_spaces = self._build_spaces("night", max_agents_in_night,
                                               max_night_spaces)
        if max_house_spaces * max_agents_in_house < max_agents or \
                max_work_spaces * max_agents_in_work < max_agents or \
                max_night_spaces * max_agents_in_night < max_agents:
            print(
                "WARNING: Not enough Spaces for all agents. `populate` will cause loop.")

    @staticmethod
    def _build_spaces(denomination, capacity, quantity):
        return [Space(denomination, capacity) for _ in range(quantity)]

    def get_agents_ids_by_status(self, status):
        return [agent.id for agent in self.agents if agent.status == status]

    def populate(self):
        print("Populating Environment")
        if self.is_populated:
            return "Environment Already Populated."
        # TODO: Avoid infinite loops and guarantee speed in space division
        for i in range(self.starting_agents):
            if i % 100 == 0:
                print(f"Agents Created: {i}/{self.starting_agents}")
            agent = Agent(identification=i)
            while not agent.spaces_id["house"]:
                house_id = np.random.randint(len(self.house_spaces))
                self.house_spaces[house_id].add_agent(agent)
            while not agent.spaces_id["work"]:
                work_id = np.random.randint(len(self.work_spaces))
                self.work_spaces[work_id].add_agent(agent)
            while not agent.spaces_id["night"]:
                night_id = np.random.randint(len(self.night_spaces))
                self.night_spaces[night_id].add_agent(agent)
            self.agents.append(agent)
        self.is_populated = True

    def start_infection(self, infected_agents):
        healthy_ids = sample(self.get_agents_ids_by_status(0), infected_agents)
        for i in healthy_ids:
            self.agents[i].infect()

    def get_status(self):
        status_list = [COVID_STAGES[agent.status] for agent in self.agents]
        return Counter(status_list)

    def execute_house_routine(self, infection_risk):
        infected = 0
        for house in self.house_spaces:
            for p1 in house.agents_id_list:
                for p2 in house.agents_id_list:
                    if self.agents[p1].status == self.agents[p2].status \
                            or self.agents[p2].status in IMMUNE_STATUS\
                            or self.agents[p1].status != 2:
                        continue
                    if self.agents[p1].status == 2 \
                            and self.agents[p2].status == 0 \
                            and random() < infection_risk:
                        self.agents[p2].infect()
                        infected += 1
        return infected

    def execute_work_routine(self, infection_risk):
        infected = 0
        for work in self.work_spaces:
            for p1 in work.agents_id_list:
                for p2 in work.agents_id_list:
                    if self.agents[p1].status == self.agents[p2].status \
                            or self.agents[p2].status in IMMUNE_STATUS \
                            or self.agents[p1].status != 2:
                        continue
                    if self.agents[p1].status == 2 \
                            and self.agents[p2].status == 0 \
                            and random() < infection_risk:
                        self.agents[p2].infect()
                        infected += 1
        return infected

    def execute_night_routine(self, infection_risk):
        # TODO: Maybe the night routine could change some nights, or even not happen for some
        infected = 0
        for night in self.night_spaces:
            for p1 in night.agents_id_list:
                for p2 in night.agents_id_list:
                    if self.agents[p1].status == self.agents[p2].status \
                            or self.agents[p2].status in IMMUNE_STATUS \
                            or self.agents[p1].status != 2:
                        continue
                    if self.agents[p1].status == 2 \
                            and self.agents[p2].status == 0 \
                            and random() < infection_risk:
                        self.agents[p2].infect()
                        infected += 1
        return infected

    def execute_end_of_day(self, incubation_time, recovery_time):
        recovered = 0
        for agent in self.agents:
            if agent.status == 1 and agent.status_age >= incubation_time:
                agent.status, agent.status_age = 2, 0
            elif agent.status == 2 and agent.status_age >= recovery_time:
                agent.status, agent.status_age = 3, 0
                recovered += 1
            else:
                agent.status_age += 1
        return recovered

    def __repr__(self):
        return f"Enviroment-> starting_agents: {self.starting_agents} | " \
               + f"agents_count: {len(self.agents)} | " \
               + f"house_spaces: {len(self.house_spaces)} | " \
               + f"work_spaces: {len(self.work_spaces)} | " \
               + f"night_spaces: {len(self.night_spaces)}"


class Simulation:
    def __init__(self, environment, base_infection_risk=0.02, incubation_time=3,
                 recovery_time=12, start_time=0):
        self.time_position = start_time
        self.environment = environment
        self.base_infection_risk = base_infection_risk
        self.incubation_time = incubation_time
        self.recovery_time = recovery_time

    def get_status(self):
        return self.environment.get_status()

    def step_time(self, print_status=False):
        if not self.environment.is_populated:
            return "Environment Not Populated Yet."
        infected = 0
        infected += self.environment.execute_house_routine(self.base_infection_risk)
        infected += self.environment.execute_night_routine(self.base_infection_risk)
        infected += self.environment.execute_night_routine(self.base_infection_risk)
        recovered = self.environment.execute_end_of_day(self.incubation_time, self.recovery_time)
        if print_status:
            print(f"End of Day: {self.time_position}\n{infected} Agent(s) Infected.\n"
                  f"{recovered} Agent(s) Recovered.\n{self.get_status()}")
        self.time_position += 1


env = Environment(max_agents=1000, max_house_spaces=220, max_work_spaces=110,
                  max_night_spaces=110)
env.populate()
env.start_infection(100)
sim = Simulation(environment=env, base_infection_risk=.02)
sim.step_time(print_status=True)
