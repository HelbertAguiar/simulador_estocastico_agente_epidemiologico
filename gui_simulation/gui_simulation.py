import dearpygui.dearpygui as dpg
import csv
import os

class Gui_simulation():

    def __init__(self, log_addr, height=None, width=None, ):
        self.log_addr = log_addr
        self.height = height
        self.width = width
        self.title = 'Simulador da Evolucao do Agent Epidemiologic'

    def generate(self):
        
        # create process to generate graph
        dpg.create_context()

        # read the log with data and assign variable series_x e series_y
        with open(self.log_addr, newline='') as csvfile:
            rows = csv.DictReader(csvfile)
            x_total_days, y_total_healthy, y_total_infected, \
            y_total_incubating, y_total_deceased, y_total_healed = map(list, zip(*[self.split(row) for row in rows]))

        # setting plot
        with dpg.window(label="simulation", tag="win"):
            with dpg.plot(label="Result of model for studying the evolution of contamination", height=self.height-100, width=self.width-100):
                dpg.add_plot_legend()
                dpg.add_plot_axis(dpg.mvXAxis, label="Days", tag="x_axis" )
                dpg.add_plot_axis(dpg.mvYAxis, label="Population", tag="y_axis")
                dpg.add_line_series(x_total_days, y_total_healthy, label="healthy", parent="y_axis", tag="series_healthy")
                dpg.add_line_series(x_total_days, y_total_infected, label="infected", parent="y_axis", tag="series_infected")
                dpg.add_line_series(x_total_days, y_total_incubating, label="incubating", parent="y_axis", tag="series_incubating")
                dpg.add_line_series(x_total_days, y_total_deceased, label="deceased", parent="y_axis", tag="series_deceased")
                dpg.add_line_series(x_total_days, y_total_healed, label="healed", parent="y_axis", tag="series_healed")

        dpg.create_viewport(title=self.title, width=self.width, height=self.height)
        dpg.setup_dearpygui()
        dpg.show_viewport()

        # show graph here
        dpg.start_dearpygui()
        # while dpg.is_dearpygui_running():
        #     dpg.render_dearpygui_frame()
        
        dpg.destroy_context()

    def split(self, row):
        return float(row['day']), float(row['total_healthy']), float(row['total_infected']), \
            float(row['total_incubating']), float(row['total_deceased']), float(row['total_healed']), 

if __name__ == "__name__":
    pass

# gui = Gui_simulation("logs" + os.path.sep + "log_2022-02-01_17h20m22s.csv", 800, 1000)
# gui.generate()