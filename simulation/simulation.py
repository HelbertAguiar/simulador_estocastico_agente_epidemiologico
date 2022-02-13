import datetime

import numpy as np

from .logger import Logger
import os


class Simulation:
    def __init__(self, environment, base_infection_risk=.02, decease_risk=.005,
                 incubation_time=3, recovery_time=12, start_time=0, gui_simulation=None):
        self.time_position = start_time
        self.environment = environment
        self.base_infection_risk = base_infection_risk
        self.incubation_time = incubation_time
        self.recovery_time = recovery_time
        self.decease_risk = decease_risk
        self.logger = self.start_logger(gui_simulation)

    @staticmethod
    def start_logger(gui_simulation: object = None):
        now = datetime.datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss")
        header = [
            "day", "total_healthy", "total_infected", "total_incubating", "total_deceased",
            "total_healed", "infected_today", "deceased_today", "recovered_today", "r0"
        ]
        log_addr = "." + os.path.sep + "logs" + os.path.sep + "log_" + now + ".csv"
        gui_simulation.set_log_addr(log_addr)
        return Logger(log_addr, header)

    def get_status(self):
        return self.environment.get_status()

    def step_time(self, print_status=False, dpg=None):
        if not self.environment.is_populated:
            return "Environment Not Populated Yet."
        infected = 0
        infected += self.environment.execute_house_routine(self.base_infection_risk)
        infected += self.environment.execute_night_routine(self.base_infection_risk)
        infected += self.environment.execute_night_routine(self.base_infection_risk)
        recovered, deceased = self.environment.execute_end_of_day(
            self.incubation_time, self.recovery_time, self.decease_risk)
        curr_status = self.get_status()

        R0 = 1 * ((np.log(self.environment.starting_agents - 1) - np.log(curr_status["healthy"])) / (self.environment.starting_agents - curr_status["healthy"] - 0))

        self.logger.write_to_log_file(
            [self.time_position, curr_status["healthy"], curr_status["infected"],
             curr_status["incubating"], curr_status["deceased"],
             curr_status["healed/immune"], infected, deceased, recovered, R0]
        )
        self.time_position += 1
        if print_status:
            print(f"________End of Day: {self.time_position}________"
                  f"\n{infected} Agent(s) Infected.\n"
                  f"{recovered} Agent(s) Recovered.\n"
                  f"{deceased} Agent(s) Deceased.\n"
                  f"{curr_status}\n"
                  f"--------------------------------")
        
        dpg.set_value('status_log', 'Processing.. (Starting infection) - Day: ' + str(self.time_position)
                        + ' - Healthy(Not contaminated): ' + str(curr_status["healthy"])
                        + ' - Infected: ' + str(infected)
                        + ' - Recovered: ' + str(recovered)
                        + ' - Deceased: ' + str(deceased)
                        + ' - Healed/Immune: ' + str(curr_status["healed/immune"])
        )

if __name__ == "__main__":
    pass
