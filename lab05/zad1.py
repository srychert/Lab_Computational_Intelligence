import pyswarms as ps
import math
import numpy as np
from pyswarms.utils.plotters import plot_cost_history
import matplotlib.pyplot as plt

def endurance(particles):
    x, y, z, u, v, w = particles
    # print(particles)
    return -(math.exp(-2*(y-math.sin(x))**2)+math.sin(z*u)+math.cos(v*w))


def f(x):
    n_particles = x.shape[0]
    j = [endurance(x[i]) for i in range(n_particles)]
    return np.array(j)



x_max = np.ones(6)
x_min = np.zeros(6)
my_bounds = (x_min, x_max)

options = {'c1': 0.5, 'c2': 0.3, 'w': 0.9}
optimizer = ps.single.GlobalBestPSO(n_particles=10, dimensions=6,
                                    options=options, bounds=my_bounds)

optimizer.optimize(f, iters=1000)
plot_cost_history(optimizer.cost_history)
iteration_of_find = optimizer.cost_history.index(optimizer.cost_history[-1]) + 1
print("Minimum found on iteration number:", iteration_of_find)
plt.show()
