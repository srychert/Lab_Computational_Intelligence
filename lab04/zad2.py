import pyswarms as ps
from pyswarms.utils.functions import single_obj as fx
from pyswarms.utils.plotters import plot_cost_history
from pyswarms.utils.plotters import plot_contour
from pyswarms.utils.plotters.formatters import Mesher
from matplotlib.animation import PillowWriter
import matplotlib.pyplot as plt
import pprint

# Set-up hyperparameters
options = {'c1': 0.5, 'c2': 0.3, 'w': 0.9}

# Call instance of GlobalBestPSO
optimizer = ps.single.GlobalBestPSO(n_particles=10, dimensions=2,
                                    options=options)

# Perform optimization
stats = optimizer.optimize(fx.sphere, iters=100)

# Obtain cost history from optimizer instance
cost_history = optimizer.cost_history

# Plot!
plot_cost_history(cost_history)
pprint.pprint(cost_history, indent=4)
iteration_of_find = cost_history.index(cost_history[-1]) + 1
print("Minimum found on iteration number:", iteration_of_find)
plt.show()

# Initialize mesher with sphere function
m = Mesher(func=fx.sphere)
# Make animation
animation = plot_contour(pos_history=optimizer.pos_history,
                         mesher=m,
                         mark=(0,0))

animation.save('plot0.gif', writer=PillowWriter(fps=10))
