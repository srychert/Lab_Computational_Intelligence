import numpy as np
import pygad
import json
import copy
import time
import pprint
from DFS import DFS

puzzles = {}
with open("puzzles.json", "r") as f:
    puzzles = json.load(f)

# from 0 to 8
board = np.array(puzzles["4"])

#definiujemy parametry chromosomu
#geny to liczby: -1 lub 0
gene_space = [-1, 0]

def makeBoardWithSoution(solution):
    board_c = copy.deepcopy(board)
    np_tuple = np.where(board_c == 0)
    cords = list(zip(np_tuple[0], np_tuple[1]))
    for idx, value in enumerate(solution):
        board_c[cords[idx]] = value
    return board_c

def rookSum(arr, idx):
    arr_1 = arr[:idx][::-1]
    arr_2 = arr[idx+1:]
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
    if x != 0 and x != -1:
        row_sum = rookSum(row, idx[1])
        col_sum = rookSum(column, idx[0])
        total_sum = row_sum + col_sum + 1
        points += abs(x - total_sum)

    if x == 0:
        row_sides, row_sum = whiteConnected(row, idx[1])
        col_sides, col_sum = whiteConnected(column, idx[0])
        if row_sum + col_sum == row_sides + col_sides:
            points += 1

    return points


def blackSum(arr, idx):
    arr_2 = arr[idx+1:]
    sum = 0
    # if first value in array is -1 add 1
    if len(arr_2) != 0 and arr_2[0] == -1:
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

    return points*2


#definiujemy funkcję fitness
def fitness_func(solution, solution_idx):
    board_s = makeBoardWithSoution(solution)
    points = 0
    dfs = DFS()

    firstA = np.argwhere(board_s != -1)[0]
    first = (firstA[0], firstA[1])

    for idx, x in np.ndenumerate(board_s):
        points -= whiteCellsPoints(x, idx, board_s)
        points -= blackCellsPoints(x, idx, board_s)

    islands = dfs.getNumberOfIslands(board_s, first)
    points -= islands - 1

    return points

fitness_function = fitness_func

#ile chromsomów w populacji - tablic z -1 i 0
#ile genow ma chromosom
sol_per_pop = board.shape[0] * board.shape[1] * 10
num_genes = 0
for i in board.flatten():
    if i == 0:
        num_genes += 1
# print(num_genes)

#ile wylaniamy rodzicow do "rozmanazania" 1/4 populacji
#ile pokolen
#ilu rodzicow zachowac (kilka procent)
num_parents_mating = int(0.25 * sol_per_pop)
num_generations = int(2 * sol_per_pop)
keep_parents = int(0.01 * sol_per_pop)
s = int(0.02 * num_generations)
saturate = "saturate_{s}".format(s = 15 if s < 15 else s)
print(sol_per_pop, num_genes, num_parents_mating, num_generations, keep_parents, saturate)

#jaki typ selekcji rodzicow?
#sss = steady, rws=roulette, rank = rankingowa, tournament = turniejowa
parent_selection_type = "sss"

#w il =u punktach robic krzyzowanie?
crossover_type = "single_point"

#mutacja ma dzialac na ilu procent genow?
#trzeba pamietac ile genow ma chromosom
mutation_type = "random"  # zamiana losowego genu
mutation_percent_genes = round(120 / num_genes, 3)  # razy długość chromosomu troche powyżej 100

#inicjacja algorytmu z powyzszymi parametrami wpisanymi w atrybuty
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


def run(tries):
    timeResults = {"time": [], "numOfGenerations": [], "fitnessValueBest": []}
    for x in range(tries):
        ga_copy = copy.deepcopy(ga_instance)
        # start time
        start_time = time.time()
        ga_copy.run()
        end_time = time.time()
        solution, solution_fitness, solution_idx = ga_copy.best_solution()
        timeResults["time"].append(round(end_time - start_time, 5))
        timeResults["numOfGenerations"].append(ga_copy.generations_completed)
        timeResults["fitnessValueBest"].append(solution_fitness)
        if solution_fitness == 0:
            print(makeBoardWithSoution(solution))

    avg = 0
    successful_runs_times = []
    for idx, fit in enumerate(timeResults["fitnessValueBest"]):
        if fit == 0:
            successful_runs_times.append(timeResults["time"][idx])

    avg = avg if len(successful_runs_times) == 0 else round(sum(successful_runs_times) / len(successful_runs_times), 5)
    timeResults["avgOfSuccessfulRuns"] = avg
    pprint.pprint(timeResults, width=200)
    print("\n")

# run(10)

#uruchomienie algorytmu
start_time = time.time()
ga_instance.run()
end_time = time.time()
print(end_time - start_time)


#podsumowanie: najlepsze znalezione rozwiazanie (chromosom+ocena)
solution, solution_fitness, solution_idx = ga_instance.best_solution()
print("Parameters of the best solution : {solution}".format(solution=solution))
print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))

print(makeBoardWithSoution(solution))

# wyswietlenie wykresu: jak zmieniala sie ocena na przestrzeni pokolen
ga_instance.plot_fitness()