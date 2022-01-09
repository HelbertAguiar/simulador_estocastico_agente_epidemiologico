from simulation import Environment, Simulation


env = Environment(max_agents=1000, max_house_spaces=220, max_work_spaces=110,
                  max_night_spaces=110)
env.populate()
env.start_infection(100)
sim = Simulation(environment=env, base_infection_risk=.02)
sim.step_time(print_status=True)