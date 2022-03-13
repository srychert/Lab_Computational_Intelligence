import pandas as pd
import matplotlib.pyplot as plt

# a)
miasta = pd.read_csv("./miasta.csv")
# print(miasta)
print(miasta.values)

# b)
miasta.loc[len(miasta.index)] = [2010, 460, 555, 405]
print(miasta)

# c) + d)
figure, axis = plt.subplots(1, 2)


def set_plot(index: int, pos, title, xlabel, ylabel):
    axis[index].legend(loc=pos)
    axis[index].set_title(title)
    axis[index].set_xlabel(xlabel)
    axis[index].set_ylabel(ylabel)


def draw_plot(index: int, city, color):
    axis[index].plot(miasta["Rok"], miasta[city], "-o", color=color, label=city)


draw_plot(0, "Gdansk", "red")
colors = ["red", "green", "blue"]

for column in miasta.columns[1:]:
    draw_plot(1, column, colors.pop(0))

for i in range(2):
    set_plot(i, "upper left", "Ludnosc w miastach Polski", "Lata", "Liczba ludnosci [w tys.]")

plt.show()
