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
        recovered = self.environment.execute_end_of_day(
            self.incubation_time, self.recovery_time)
        if print_status:
            print(f"End of Day: {self.time_position}\n{infected} Agent(s) Infected.\n"
                  f"{recovered} Agent(s) Recovered.\n{self.get_status()}")
        self.time_position += 1

if __name__ == "__main__":
    pass
