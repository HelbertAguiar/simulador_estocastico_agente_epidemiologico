import datetime
import numpy as np
from .logger import Logger
import os


class Simulation:
    def __init__(self, environment, rate_infection=.002, rate_decease=.005,
                 min_incubation_time=2, min_recovery_time=7, start_time=0,
                 gui_simulation:object=None, hospitalization_chance=.3):
        self.time_position = start_time
        self.environment = environment
        self.rate_infection = rate_infection
        self.min_incubation_time = min_incubation_time
        self.min_recovery_time = min_recovery_time
        self.rate_decease = rate_decease
        self.logger = self.start_logger(gui_simulation)
        self.hospitalization_chance = hospitalization_chance

    @staticmethod
    def start_logger(gui_simulation: object = None):
        now = datetime.datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss")
        header = [
            "day", "total_healthy", "total_infected", "total_incubating", "total_deceased",
            "total_healed", "total_hospitalized", "infected_today", "deceased_today",
            "recovered_today"
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
        infected += self.environment.execute_house_routine(self.rate_infection)
        infected += self.environment.execute_work_routine(self.rate_infection)
        infected += self.environment.execute_night_routine(self.rate_infection)
        recovered, deceased = self.environment.execute_end_of_day(
            self.min_incubation_time, self.min_recovery_time, self.rate_decease,
            self.hospitalization_chance)
        curr_status = self.get_status()

        self.logger.write_to_log_file(
            [self.time_position, curr_status["healthy"], curr_status["infected"],
             curr_status["incubating"], curr_status["deceased"],
             curr_status["healed/immune"],curr_status["hospitalized"],
             infected, deceased, recovered]
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
