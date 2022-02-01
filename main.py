import sys
sys.dont_write_bytecode = True
from simulation import Environment, Simulation
from gui_simulation import Gui_simulation
import os

# TODO: Better parameter handling projectwide
# TODO:
env = Environment(max_agents=100000, max_house_spaces=25000, max_work_spaces=10000,
                  max_night_spaces=7500)
env.populate()
env.start_infection(1, skip_incubation=True)
print(env.get_status())
sim = Simulation(environment=env, base_infection_risk=.025, decease_risk=.015)
sim.step_time(print_status=True)

for _ in range(365):
    sim.step_time(print_status=False)

gui = Gui_simulation(sim.log_addr.replace(os.path.sep, "/"), 800, 1000)
gui.generate()