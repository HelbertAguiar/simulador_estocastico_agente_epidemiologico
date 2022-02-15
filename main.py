import sys
sys.dont_write_bytecode = True
from gui_simulation import GuiSimulator


gui = GuiSimulator(height=1000, width=1200, maximize=True)
gui.render_screen_initial()
