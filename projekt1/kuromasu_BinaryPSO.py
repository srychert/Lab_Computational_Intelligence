import argparse
import concurrent.futures
import copy
import json
import time

import numpy as np
import pyswarms as ps
from pyswarms.utils.plotters import plot_cost_history
import matplotlib.pyplot as plt

from DFS import DFS

parser = argparse.ArgumentParser(description='flags for selecting the puzzle and the number of runs of the algorithm')
parser.add_argument('--p', action="store", dest='p', default="0")
parser.add_argument('--r', action="store", dest='r', default=0)
args = parser.parse_args()

# load puzzles from file
puzzles = {}
with open("puzzles.json", "r") as f:
    puzzles = json.load(f)

# make a board for puzzle
board = np.array(puzzles[args.p])


def makeBoardWithSoution(solution):
    board_c = copy.deepcopy(board)
    np_tuple = np.where(board_c == 0)
    cords = list(zip(np_tuple[0], np_tuple[1]))
    for idx, value in enumerate(solution):
        board_c[cords[idx]] = value

    return board_c


def rookSum(arr, idx):
    arr_1 = arr[:idx][::-1]
    arr_2 = arr[idx + 1:]
    sum = 0
    for i in arr_1:
        if i == 1:
            break
        else:
            sum += 1
    for i in arr_2:
        if i == 1:
            break
        else:
            sum += 1
    return sum


def whiteConnected(arr, idx):
    arr_1 = arr[:idx][::-1]
    arr_2 = arr[idx + 1:]
    sides = 0
    sum = 0

    if len(arr_1) != 0:
        sides += 1
        if arr_1[0] == 1:
            sum += 1

    if len(arr_2) != 0:
        sides += 1
        if arr_2[0] == 1:
            sum += 1

    return (sides, sum)


def whiteCellsPoints(x, idx, board_s):
    row = board_s[idx[0], :]
    column = board_s[:, idx[1]]
    points = 0
    # only numbered cells
    if x != 0 and x != 1:
        # sum the number of cells vertically and horizontally from this white cell until black cells or edge
        row_sum = rookSum(row, idx[1])
        col_sum = rookSum(column, idx[0])
        # add itself to total
        total_sum = row_sum + col_sum + 1
        # final result is absolute difference between cell value and sum
        points += abs(x - total_sum)

    # check if empty cell is not cornered by black cells
    if x == 0:
        row_sides, row_sum = whiteConnected(row, idx[1])
        col_sides, col_sum = whiteConnected(column, idx[0])
        if row_sum + col_sum == row_sides + col_sides:
            points += 1

    return points


def blackSum(arr, idx):
    arr_2 = arr[idx + 1:]
    sum = 0
    if len(arr_2) != 0:
        if arr_2[0] == 1:
            sum += 1

    return sum


def blackCellsPoints(x, idx, board_s):
    points = 0
    if x == 1:
        row = board_s[idx[0], :]
        column = board_s[:, idx[1]]
        # number of black cells adjacent to right and down to this black cell
        points += blackSum(row, idx[1])
        points += blackSum(column, idx[0])

    return points * 2


# definiujemy funkcję fitness
def fitness_func(solution):
    # board for solution
    board_s = makeBoardWithSoution(solution)
    points = 0
    # deep first search object
    dfs = DFS()
    # find starting point for dfs
    firstA = np.argwhere(board_s != 1)[0]
    first = (firstA[0], firstA[1])

    # calculate points
    for idx, x in np.ndenumerate(board_s):
        points += whiteCellsPoints(x, idx, board_s)
        points += blackCellsPoints(x, idx, board_s)

    # check if there is only one island else give punishment points
    islands = dfs.getNumberOfIslands(board_s, first)
    points += 2 ** (islands - 1) - 1

    return points


def f(x):
    n_particles = x.shape[0]
    j = [fitness_func(x[i]) for i in range(n_particles)]
    return np.array(j)


options = {'c1': 0.5, 'c2': 0.3, 'w':0.9, 'k':2, 'p':1}

dimensions = 0
for i in board.flatten():
    if i == 0:
        dimensions += 1


optimizer = ps.discrete.BinaryPSO(n_particles=100, dimensions=dimensions,
options=options)
optimizer.optimize(f, iters=1000, verbose=True)

cost_history = optimizer.cost_history
iteration_of_find = cost_history.index(cost_history[-1]) + 1
print("Minimum found on iteration number:", iteration_of_find)
plot_cost_history(cost_history)
plt.show()


# function for running algorithm
# x is used for multiprocessing; see in main
def runOptimizer(x):
    optimizer_copy = copy.deepcopy(optimizer)

    start_time = time.time()
    optimizer_copy.optimize(f, iters=300, verbose=True)
    end_time = time.time()

    resutlTime = round(end_time - start_time, 5)

    cost_history = optimizer_copy.cost_history

    return {"time": resutlTime, "cost_history": cost_history}


# if __name__ == "__main__":
#
#     def run(tries):
#
#         results = []
#         with concurrent.futures.ProcessPoolExecutor() as executor:
#             # make list of len = tries
#             l = list(range(0, tries))
#             # run tries number of processes
#             pool = executor.map(runOptimizer, l)
#             for res in pool:
#                 results.append(res)
#
#         succesTimes = []
#         costHistory = []
#         for res in results:
#             r = {i: res[i] for i in res if i != 'solution'}
#             print(r)
#             succesTimes.append(res["time"])
#             costHistory.append(res["cost_history"])
#
#         if len(succesTimes) > 0:
#             print("average time of successful runs:                 ", np.average(np.array(succesTimes)))
#             # print("average generation completed of successful runs: ", np.average(np.array(successGen)))
#             print("success: {s}%".format(s=len(succesTimes) / int(args.r) * 100))
#         else:
#             print("No success runs!")
#
#
#     run(int(args.r))
