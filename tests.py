from simulation import Environment, Simulation
from time import sleep


# TODO: Better parameter handling projectwide
# TODO:
env = Environment(max_agents=500, max_house_spaces=120, max_work_spaces=75,
                  max_night_spaces=75)
env.populate()
env.start_infection(5, skip_incubation=True)
print(env.get_status())
sim = Simulation(environment=env, base_infection_risk=.02)
sim.step_time(print_status=True)

for _ in range(300):
    sim.step_time(print_status=True)
    sleep(2)