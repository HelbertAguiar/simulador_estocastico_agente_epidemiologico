""" Module with class to handle process of environment of simulation"""

from collections import Counter
from random import random, sample
import numpy as np
from .space import Space
from .agent import Agent


COVID_STAGES = {0: "healthy", 1: "incubating", 2: "infected",
                3: "healed/immune", 4: "deceased", 5: "hospitalized"}
IMMUNE_STATUS = [1, 2, 3, 4, 5]


class Environment:
    """ Class with functions to Environment """
    def __init__(self, max_agents, max_house_spaces, max_work_spaces,
                 max_night_spaces, max_agents_in_house=5,
                 max_agents_in_work=20, max_agents_in_night=30,
                 incubation_phase=True, dpg=None):
        self.dpg = dpg
        self.is_populated = False
        self.starting_agents = max_agents
        self.agents = []
        self.incubation_phase = incubation_phase
        self.house_spaces = self._build_spaces("house", max_agents_in_house, max_house_spaces)
        self.work_spaces = self._build_spaces("work", max_agents_in_work, max_work_spaces)
        self.night_spaces = self._build_spaces("night", max_agents_in_night, max_night_spaces)
        if max_house_spaces * max_agents_in_house < max_agents or \
                max_work_spaces * max_agents_in_work < max_agents or \
                max_night_spaces * max_agents_in_night < max_agents:
            print(
                "WARNING: Not enough Spaces for all agents. `populate` will cause loop.")

    @staticmethod
    def _build_spaces(denomination, capacity, quantity):
        return [Space(denomination, capacity) for _ in range(quantity)]

    def get_agents_ids_by_status(self, status):
        """ get agents ids by status """
        return [agent.id for agent in self.agents if agent.status == status]

    def populate(self):
        """ Populate environment """
        print("Populating Environment")
        if self.is_populated:
            return "Environment Already Populated."
        for i in range(self.starting_agents):
            if i % 100 == 0:
                print(f"Agents Created: {i}/{self.starting_agents}")
                self.dpg.set_value(
                    'status_log', 'Processing.. (Creating individuals) - ' +
                    f"Agents Created: {i}/{self.starting_agents}")
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

    def start_infection(self, infected_agents, skip_incubation=False):
        """ Starts infection """
        healthy_ids = sample(self.get_agents_ids_by_status(0), infected_agents)
        for i in healthy_ids:
            self.agents[i].infect(incubation_phase=(not skip_incubation))

    def get_status(self):
        """ Ger counter of status"""
        status_list = [COVID_STAGES[agent.status] for agent in self.agents]
        return Counter(status_list)

    def execute_house_routine(self, rate_infection):
        """ Introduce interaction on house among agents """
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
                            and random() < rate_infection:
                        self.agents[p2].infect(self.incubation_phase)
                        infected += 1
        return infected

    def execute_work_routine(self, rate_infection):
        """ Introduce interaction on work among agents """
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
                            and random() < rate_infection:
                        self.agents[p2].infect()
                        infected += 1
        return infected

    def execute_night_routine(self, rate_infection):
        """ Introduce interaction on night among agents """
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
                            and random() < rate_infection:
                        self.agents[p2].infect()
                        infected += 1
        return infected

    def execute_end_of_day(self, min_incubation_time, min_recovery_time, deceased_risk,
                           hosp_chance):
        """ Calculate result of interaction on routines """
        recovered, deceased = 0, 0
        for agent in self.agents:
            if agent.status == 1 and agent.status_age >= min_incubation_time \
                    and np.random.normal() > 1.3:
                agent.status, agent.status_age = (5, 0) if random() < hosp_chance else (2, 0)
            elif (agent.status == 2 and random() < (deceased_risk * (1+agent.risk_factor))) \
                    or (agent.status == 5
                        and random() < ((deceased_risk)/2 * (1+agent.risk_factor))):
                agent.status, agent.status_age = 4, 0
                deceased += 1
            elif agent.status in [2, 5] and agent.status_age >= min_recovery_time \
                    and np.random.normal() > 1.3:
                agent.status, agent.status_age = 3, 0
                recovered += 1
            else:
                agent.status_age += 1
        return recovered, deceased

    def __repr__(self):
        return f"Enviroment-> starting_agents: {self.starting_agents} | " \
               + f"agents_count: {len(self.agents)} | " \
               + f"house_spaces: {len(self.house_spaces)} | " \
               + f"work_spaces: {len(self.work_spaces)} | " \
               + f"night_spaces: {len(self.night_spaces)}"


if __name__ == "__main__":
    pass
