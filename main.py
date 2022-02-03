import sys
sys.dont_write_bytecode = True
from gui_simulation import Gui_simulation

gui = Gui_simulation(height = 1000, width = 1200, maximize = True)
gui.render_screen_initial()