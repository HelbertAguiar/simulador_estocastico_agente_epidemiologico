import pandas as pd
import matplotlib.pyplot as plt
import os

df = pd.read_csv("logs" + os.path.sep + "log_2022-01-31_18h15m20s.csv")

f, axs = plt.subplots(2, 2, figsize=(12, 8))
# f = plt.figure(figsize=(10, 3))
# ax = f.add_subplot(121)
# ax2 = f.add_subplot(122)
# ax3 = f.add_subplot(111)
# ax4 = f.add_subplot(211)

axs[0, 0].set_title("Total de Infectados Por Dia")
axs[0, 0].plot(df.day, df.total_infected, color="red")

axs[0, 1].set_title("Total de Saudáveis Por Dia")
axs[0, 1].plot(df.day, df.total_healthy, color="green")

axs[1, 0].set_title("Total de Mortos Por Dia")
axs[1, 0].plot(df.day, df.total_deceased, color="black")

axs[1, 1].set_title("Total de Curados Por Dia")
axs[1, 1].plot(df.day, df.total_healed, color="blue")
plt.tight_layout()
plt.show()


plt.plot(df.day[:260], df.infected_today[:260], color="blue")
plt.show()