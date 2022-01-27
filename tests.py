from simulation import Environment, Simulation
from time import sleep


# TODO: Better parameter handling projectwide
# TODO:
env = Environment(max_agents=100000, max_house_spaces=25000, max_work_spaces=10000,
                  max_night_spaces=7500)
env.populate()
env.start_infection(1, skip_incubation=True)
print(env.get_status())
sim = Simulation(environment=env, base_infection_risk=.01, decease_risk=.005)
sim.step_time(print_status=True)

for _ in range(500):
    sim.step_time(print_status=False)
    # sleep(2)