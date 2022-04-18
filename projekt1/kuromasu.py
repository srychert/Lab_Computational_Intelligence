import argparse
import concurrent.futures
import copy
import json
import time

import numpy as np
import pygad

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
        if i == -1:
            break
        else:
            sum += 1
    for i in arr_2:
        if i == -1:
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
        if arr_1[0] == -1:
            sum += 1

    if len(arr_2) != 0:
        sides += 1
        if arr_2[0] == -1:
            sum += 1

    return (sides, sum)


def whiteCellsPoints(x, idx, board_s):
    row = board_s[idx[0], :]
    column = board_s[:, idx[1]]
    points = 0
    # only numbered cells
    if x != 0 and x != -1:
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
        if arr_2[0] == -1:
            sum += 1

    return sum


def blackCellsPoints(x, idx, board_s):
    points = 0
    if x == -1:
        row = board_s[idx[0], :]
        column = board_s[:, idx[1]]
        # number of black cells adjacent to right and down to this black cell
        points += blackSum(row, idx[1])
        points += blackSum(column, idx[0])

    return points * 2


# definiujemy funkcję fitness
def fitness_func(solution, solution_idx):
    # board for solution
    board_s = makeBoardWithSoution(solution)
    points = 0
    # deep first search object
    dfs = DFS()
    # find starting point for dfs
    firstA = np.argwhere(board_s != -1)[0]
    first = (firstA[0], firstA[1])

    # calculate points
    for idx, x in np.ndenumerate(board_s):
        points -= whiteCellsPoints(x, idx, board_s)
        points -= blackCellsPoints(x, idx, board_s)

    # check if there is only one island else give punishment points
    islands = dfs.getNumberOfIslands(board_s, first)
    points -= 2 ** (islands - 1) - 1

    return points


fitness_function = fitness_func

gene_space = [-1, 0]

# population size
sol_per_pop = board.shape[0] * board.shape[1] * 10
# calc gene length form board
num_genes = 0
for i in board.flatten():
    if i == 0:
        num_genes += 1

num_parents_mating = int(0.25 * sol_per_pop)
num_generations = int(2 * sol_per_pop)
keep_parents = int(0.01 * sol_per_pop)
s = int(0.02 * num_generations)
saturate = "saturate_{s}".format(s=15 if s < 15 else s)

# sss = steady, rws=roulette, rank = rankingowa, tournament = turniejowa
parent_selection_type = "sss"

crossover_type = "single_point"

mutation_type = "random"
# small boards - smaller mutation percent and bigger for bigger boards
mutation_percent_genes = 120 / num_genes if num_genes <= 50 else 100 * (2 / num_genes)

# make algorithm instance
ga_instance = pygad.GA(gene_space=gene_space,
                       gene_type=int,
                       num_generations=num_generations,
                       num_parents_mating=num_parents_mating,
                       fitness_func=fitness_function,
                       sol_per_pop=sol_per_pop,
                       num_genes=num_genes,
                       parent_selection_type=parent_selection_type,
                       keep_parents=keep_parents,
                       crossover_type=crossover_type,
                       mutation_type=mutation_type,
                       mutation_percent_genes=mutation_percent_genes,
                       stop_criteria=["reach_0", saturate])


# function for running algorithm
# x is used for multiprocessing; see in main
def runGA(x):
    ga_copy = copy.deepcopy(ga_instance)

    start_time = time.time()
    ga_copy.run()
    end_time = time.time()

    resutlTime = round(end_time - start_time, 5)

    solution, solution_fitness, generations_completed = ga_copy.best_solution()

    if solution_fitness == 0:
        print(makeBoardWithSoution(solution))

    return {"fitness": solution_fitness, "time": resutlTime, "gen_com": generations_completed, "solution": solution}


if __name__ == "__main__":

    def run(tries):
        print("sol_per_pop:", sol_per_pop, "num_genes:", num_genes, "num_parents_mating:",
              num_parents_mating, "num_generations:",
              num_generations, "keep_parents:", keep_parents, saturate)

        results = []
        with concurrent.futures.ProcessPoolExecutor() as executor:
            # make list of len = tries
            l = list(range(0, tries))
            # run tries number of processes
            pool = executor.map(runGA, l)
            for res in pool:
                results.append(res)

        succesTimes = []
        for res in results:
            r = {i: res[i] for i in res if i != 'solution'}
            print(r)
            if res["fitness"] == 0:
                succesTimes.append(res["time"])

        if len(succesTimes) > 0:
            print(np.average(np.array(succesTimes)))
        else:
            print("No success runs!")


    run(int(args.r))
