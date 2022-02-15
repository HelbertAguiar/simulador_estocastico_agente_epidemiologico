""" Gui Simulator Class"""
import csv
import timeit
import dearpygui.dearpygui as dpg
import simulation.simulation
import simulation.environment


class GuiSimulator():
    """ Interface GUI """
    # path to adress log
    log_addr = None

    # amount days to simulate
    days_to_simulate = 365

    # add variable to run "set_color_series()" only time on execution
    first_execution = False

    # calculate values of each series on plot
    x_total_days = None
    x_total_days_real = None
    y_total_healthy = None
    y_total_infected = None
    y_total_incubating = None
    y_total_deceased = None
    y_total_healed = None
    y_total_hospitalized = None

    y_real_infected = None
    y_ratio_real = None
    population_bh = 2722000

    # parameters of condition initials fo environment
    max_agents = None
    max_house_space = None
    max_work_space = None
    max_night_space = None
    max_agents_in_house = None
    max_agents_in_work = None
    max_agents_in_night = None

    # below parameters epidemiologic
    # gama = duration of illness
    # sigma = estimated incubation period of the disease
    min_recovery_time = None
    min_incubation_time = None
    # parameters relationship among people (interactions)
    # beta = the rate at which infectious people interact with others
    rate_infection = None
    rate_decease = None

    # parameters of plot
    height = None
    width = None
    maximize = None
    title = None

    # rate update frame/plot
    RATE_UPDATE_FRAME = 7

    def __init__(self, height=None, width=None, maximize: bool = False):
        self.height = height
        self.width = width
        self.maximize = maximize
        self.title = 'Simulator of Evolution of Agent Epidemiologic'

    def render_screen_initial(self):
        """ create 'process' to generate graph"""
        dpg.create_context()
        dpg.create_viewport(
            title=self.title, width=self.width, height=self.height)

        # create btn START, RESET, INPUT_PARAMETERS
        with dpg.window(label='simulation', tag='win1', no_title_bar=False, width=self.width, height=self.height, pos=[180, 0]):
            dpg.add_button(label='Reset', callback=self.btn_reset_simulate,
                           width=250, height=25, tag='btn_reset', pos=[492, 303])
            dpg.add_input_int(
                default_value=180, label='days_to_simulate', tag='days_to_simulate', step=1)
            dpg.add_input_int(default_value=10000,
                              label='max_agents', tag='max_agents', step=1000)
            dpg.add_input_int(
                default_value=2500, label='max_house_space', tag='max_house_space', step=500)
            dpg.add_input_int(
                default_value=4, label='max_agents_in_house', tag='max_agents_in_house', step=1)
            dpg.add_input_int(
                default_value=1000, label='max_work_space', tag='max_work_space', step=500)
            dpg.add_input_int(
                default_value=20, label='max_agents_in_work', tag='max_agents_in_work', step=1)
            dpg.add_input_int(
                default_value=750, label='max_night_space', tag='max_night_space', step=500)
            dpg.add_input_int(
                default_value=30, label='max_agents_in_night', tag='max_agents_in_night', step=1)
            dpg.add_input_int(
                default_value=10, label='min_recovery_time', tag='min_recovery_time', step=1)
            dpg.add_input_int(
                default_value=3, label='min_incubation_time', tag='min_incubation_time', step=1)
            dpg.add_input_float(
                default_value=.020, label='rate_infection', tag='rate_infection', step=.001)
            dpg.add_input_float(
                default_value=.001, label='rate_decease', tag='rate_decease', step=.001)
            dpg.add_button(label='Start', callback=self.btn_start_simulate,
                           width=250, height=25, tag='btn_start')
            dpg.add_spacer(height=5)
            dpg.add_text(default_value='Waiting start', tag='status_log')
            dpg.add_spacer(height=5)
            dpg.add_separator()
            dpg.add_spacer(height=5)
            dpg.add_plot(label="Result of model of evolution of infection",
                         height=self.height-570, width=self.width-100, tag="plot", query=True)
            dpg.add_plot_legend(parent="plot")
            dpg.add_plot_axis(dpg.mvXAxis, label="Days",
                              tag="x_axis", parent="plot")
            dpg.add_plot_axis(dpg.mvYAxis, label="Population",
                              tag="y_axis", parent="plot")

        dpg.setup_dearpygui()
        dpg.show_viewport()
        if self.maximize is True:
            dpg.maximize_viewport()
        dpg.start_dearpygui()

    def btn_start_simulate(self):
        """ Start simulation """
        time_start = timeit.default_timer()
        self.plot_delete_series_data()
        self.get_parameters_screen()

        env = simulation.environment.Environment(
            max_agents=self.max_agents, max_house_spaces=self.max_house_space,
            max_work_spaces=self.max_work_space, max_night_spaces=self.max_night_space,
            max_agents_in_house=self.max_agents_in_house, max_agents_in_work=self.max_agents_in_work,
            max_agents_in_night=self.max_agents_in_night, dpg=dpg)

        env.populate()
        env.start_infection(1, skip_incubation=True)

        sim = simulation.simulation.Simulation(
            environment=env, rate_infection=self.rate_infection,
            rate_decease=self.rate_decease, GuiSimulator=self,
            min_recovery_time=self.min_recovery_time, min_incubation_time=self.min_incubation_time
        )

        if self.first_execution is False:
            self.set_color_series()
        counter_steps_to_plot_new_series_data = 0
        # update frame|plot each week ( 7 days )
        step_days_to_plot_new_series_data = self.RATE_UPDATE_FRAME
        for _ in range(self.days_to_simulate):
            sim.step_time(print_status=False, dpg=dpg)
            counter_steps_to_plot_new_series_data += 1
            if counter_steps_to_plot_new_series_data == step_days_to_plot_new_series_data:
                counter_steps_to_plot_new_series_data = 0
                self.read_log_file()
                self.read_dataset()
                self.normalize_y_real_infected()
                self.plot_delete_series_data()
                self.plot_add_series_data()

        print('Completed simulation..')

        self.read_log_file()
        self.read_dataset()
        self.normalize_y_real_infected()
        self.plot_delete_series_data()
        self.plot_add_series_data()

        time_stop = timeit.default_timer()

        status_log = 'Completed simulation. ' + \
            str(env.get_status()).replace(
                'Counter({', 'Total(').replace(')}', '')
        status_log = status_log + ' || Time Execution:' + \
            str(round(time_stop - time_start, 0)) + ' seconds'
        dpg.set_value('status_log', status_log)

    def btn_reset_simulate(self):
        """ Reset parameters on GUI """
        dpg.set_value('days_to_simulate', 180)
        dpg.set_value('max_agents', 10000)
        dpg.set_value('max_house_space', 2500)
        dpg.set_value('max_agents_in_house', 4)
        dpg.set_value('max_work_space', 1000)
        dpg.set_value('max_agents_in_work', 20)
        dpg.set_value('max_night_space', 750)
        dpg.set_value('max_agents_in_night', 30)
        dpg.set_value('min_recovery_time', 10)
        dpg.set_value('min_incubation_time', 3)
        dpg.set_value('rate_infection', .020)
        dpg.set_value('rate_decease', .001)
        if dpg.does_item_exist('series_healthy'):
            dpg.delete_item('series_healthy')
        if dpg.does_item_exist('series_infected'):
            dpg.delete_item('series_infected')
        if dpg.does_item_exist('series_incubating'):
            dpg.delete_item('series_incubating')
        if dpg.does_item_exist('series_hospitalized'):
            dpg.delete_item('series_hospitalized')
        if dpg.does_item_exist('series_deceased'):
            dpg.delete_item('series_deceased')
        if dpg.does_item_exist('series_healed'):
            dpg.delete_item('series_healed')
        if dpg.does_item_exist('series_real'):
            dpg.delete_item('series_real')
        dpg.set_value('status_log', 'Waiting start')

    def read_log_file(self):
        """ Read log file """
        with open(self.log_addr, newline='', encoding='utf-8') as csvfile:
            rows = csv.DictReader(csvfile)
            self.x_total_days, self.y_total_healthy, \
                self.y_total_infected, self.y_total_incubating, \
                self.y_total_deceased, self.y_total_healed, self.y_total_hospitalized \
                = map(list, zip(*[self.split(row) for row in rows]))

    def read_dataset(self):
        """ Read dataset file """
        with open("./dataset/covidbh.csv", newline='', encoding='utf-8') as csvfile:
            rows = csv.DictReader(csvfile, delimiter=';')
            self.x_total_days_real, self.y_real_infected \
                = map(list, zip(*[self.split_dataset(row) for row in rows]))

    def normalize_y_real_infected(self):
        """ Prepare to Apply ratio on each value on series real """
        self.y_real_infected = list(
            map(self.apply_ratio, self.y_real_infected))

    def apply_ratio(self, element):
        """ Apply ratio on each value on series real """
        return float(element * self.y_ratio_real)

    def plot_add_series_data(self):
        """ Add series on graph """
        dpg.add_line_series(self.x_total_days, self.y_total_healthy,
                            label="healthy", parent="y_axis", tag="series_healthy")
        dpg.fit_axis_data("x_axis")
        dpg.fit_axis_data("y_axis")
        dpg.add_line_series(self.x_total_days, self.y_total_infected,
                            label="infected", parent="y_axis", tag="series_infected")
        dpg.add_line_series(self.x_total_days, self.y_total_incubating,
                            label="incubating", parent="y_axis", tag="series_incubating")
        dpg.add_line_series(self.x_total_days, self.y_total_hospitalized,
                            label="hospitalized", parent="y_axis", tag="series_hospitalized")
        dpg.add_line_series(self.x_total_days, self.y_total_deceased,
                            label="deceased", parent="y_axis", tag="series_deceased")
        dpg.add_line_series(self.x_total_days, self.y_total_healed,
                            label="healed", parent="y_axis", tag="series_healed")
        dpg.add_line_series(self.x_total_days, self.y_real_infected,
                            label="real", parent="y_axis", tag="series_real")
        dpg.bind_item_theme("series_healthy", "green")
        dpg.bind_item_theme("series_infected", "yellow")
        dpg.bind_item_theme("series_incubating", "gray")
        dpg.bind_item_theme("series_hospitalized", "pink")
        dpg.bind_item_theme("series_deceased", "red")
        dpg.bind_item_theme("series_healed", "blue")
        dpg.bind_item_theme("series_real", "white")

    def set_color_series(self):
        """ Set series color on graph"""
        self.first_execution = True
        with dpg.theme(tag="green"):
            with dpg.theme_component(dpg.mvLineSeries):
                dpg.add_theme_color(dpg.mvPlotCol_Line,
                                    (0, 255, 0), category=dpg.mvThemeCat_Plots)

        with dpg.theme(tag="red"):
            with dpg.theme_component(dpg.mvLineSeries):
                dpg.add_theme_color(dpg.mvPlotCol_Line,
                                    (255, 0, 0), category=dpg.mvThemeCat_Plots)

        with dpg.theme(tag="blue"):
            with dpg.theme_component(dpg.mvLineSeries):
                dpg.add_theme_color(dpg.mvPlotCol_Line,
                                    (0, 0, 255), category=dpg.mvThemeCat_Plots)

        with dpg.theme(tag="gray"):
            with dpg.theme_component(dpg.mvLineSeries):
                dpg.add_theme_color(
                    dpg.mvPlotCol_Line, (128, 128, 128), category=dpg.mvThemeCat_Plots)

        with dpg.theme(tag="yellow"):
            with dpg.theme_component(dpg.mvLineSeries):
                dpg.add_theme_color(
                    dpg.mvPlotCol_Line, (255, 255, 0), category=dpg.mvThemeCat_Plots)

        with dpg.theme(tag="pink"):
            with dpg.theme_component(dpg.mvLineSeries):
                dpg.add_theme_color(
                    dpg.mvPlotCol_Line, (255, 0, 255), category=dpg.mvThemeCat_Plots)

        with dpg.theme(tag="white"):
            with dpg.theme_component(dpg.mvLineSeries):
                dpg.add_theme_color(
                    dpg.mvPlotCol_Line, (255, 255, 255), category=dpg.mvThemeCat_Plots)

    def plot_delete_series_data(self):
        """ Delete series on graph"""
        if dpg.does_item_exist('series_healthy'):
            dpg.delete_item('series_healthy')
        if dpg.does_item_exist('series_infected'):
            dpg.delete_item('series_infected')
        if dpg.does_item_exist('series_incubating'):
            dpg.delete_item('series_incubating')
        if dpg.does_item_exist('series_hospitalized'):
            dpg.delete_item('series_hospitalized')
        if dpg.does_item_exist('series_deceased'):
            dpg.delete_item('series_deceased')
        if dpg.does_item_exist('series_healed'):
            dpg.delete_item('series_healed')
        if dpg.does_item_exist('series_real'):
            dpg.delete_item('series_real')

    def get_parameters_screen(self):
        """ Get parameters on inputs on GUI Simulator"""
        self.days_to_simulate = int(dpg.get_value('days_to_simulate'))
        self.max_agents = dpg.get_value('max_agents')
        self.max_house_space = dpg.get_value('max_house_space')
        self.max_agents_in_house = dpg.get_value('max_agents_in_house')
        self.max_work_space = dpg.get_value('max_work_space')
        self.max_agents_in_work = dpg.get_value('max_agents_in_work')
        self.max_night_space = dpg.get_value('max_night_space')
        self.max_agents_in_night = dpg.get_value('max_agents_in_night')
        self.min_recovery_time = dpg.get_value('min_recovery_time')
        self.min_incubation_time = dpg.get_value('min_incubation_time')
        self.rate_infection = dpg.get_value('rate_infection')
        self.rate_decease = dpg.get_value('rate_decease')
        self.y_ratio_real = float(self.max_agents) / float(self.population_bh)

    def set_log_addr(self, addr):
        """ Set adress of file log """
        self.log_addr = addr

    def split(self, row):
        """ Split the log file """
        return float(row['day']), float(row['total_healthy']), \
            float(row['total_infected']), float(row['total_incubating']), \
            float(row['total_deceased']), float(row['total_healed']), \
            float(row['total_hospitalized'])

    def split_dataset(self, row):
        """ Split the dataset file """
        return float(row['day']), float(row['casesAmount']), \



if __name__ == "__name__":
    pass
