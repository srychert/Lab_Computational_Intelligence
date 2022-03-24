import pygad
import numpy
from matplotlib import pyplot as plt
from matplotlib import animation
import cv2

# wczytaj obraz jako 2d numpy array w odcieniach szarości (0-255)
img = cv2.imread("maze.jpeg", 0)
# zamień wartości większe od 0 na 1 (czarno biały obraz)
img[img > 0] = 1
# kopia pomocnicza
S = numpy.copy(img)
# Początek i koniec labirytnu
start = [1, 1]
end = [10, 10]
# Dostępne ruchy [x, y]; x -> góra,dół; y -> lewo,prawo
moves = {
        0: [0, 1],   # R
        1: [0, -1],  # L
        2: [1, 0],   # D
        3: [-1, 0],  # U
    }

#definiujemy parametry chromosomu
#geny to liczby: 0, 1, 2, 3 odpowiadające ruchom ruchom
gene_space = [0, 1, 2, 3]

# Sprawdamy czy następna pozycja po wykonaniu ruchu jest dozwolona
def check_if_legal(move, curr_pos):
    x_move, y_move = move
    x_curr, y_curr = curr_pos
    x_new = x_move + x_curr
    y_new = y_move + y_curr

    # check if move in bounds
    if x_new < 0 or y_new < 0:
        return False
    if x_new >= S.shape[0]:
        return False
    if y_new >= S.shape[1]:
        return False

    # check if move is on the black
    if S[x_new][y_new] == 0:
        return False
    return True


# odległość taksówkowa (dodajemy pion i poziom)
def calcDistance(start, end):
    x_start, y_start = start
    x_end, y_end = end
    return abs(x_start - x_end) + abs(y_start - y_end)


#definiujemy funkcję fitness
def fitness_func(solution, solution_idx):
    current = start
    points = 0
    for move in solution:
        # jeżeli dotarliśmy do końca nie sprawdzamy reszty
        if calcDistance(current, end) == 0:
            break
        if check_if_legal(moves[move], current):
            current = [current[0]+moves[move][0], current[1]+moves[move][1]]
        else:
            # jeżeli ruch nie jest dozwolony nakładamy karę
            points += -calcDistance(start, end)
            break
    return -calcDistance(current, end) + points

fitness_function = fitness_func

#ile chromsomów w populacji
#ile genow ma chromosom
sol_per_pop = 100
num_genes = 30

#ile wylaniamy rodzicow do "rozmanazania" (okolo 50% populacji)
#ile pokolen
#ilu rodzicow zachowac (kilka procent)
num_parents_mating = 15
num_generations = 1000
keep_parents = 2

#jaki typ selekcji rodzicow?
#sss = steady, rws=roulette, rank = rankingowa, tournament = turniejowa
parent_selection_type = "sss"

#w il =u punktach robic krzyzowanie?
crossover_type = "single_point"

#mutacja ma dzialac na ilu procent genow?
#trzeba pamietac ile genow ma chromosom
mutation_type = "random"
mutation_percent_genes = 4

#inicjacja algorytmu z powyzszymi parametrami wpisanymi w atrybuty
ga_instance = pygad.GA(gene_space=gene_space,
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
                       stop_criteria=["reach_0", "saturate_200"])
ga_instance.run()

#wartości rozwiązania:
solution, solution_fitness, solution_idx = ga_instance.best_solution()


img[start[0]][start[1]] = 2
img[end[0]][end[1]] = 2
x_c, y_c = start
route = []
number_of_moves = 0
for moved in solution:
    number_of_moves += 1
    x_m, y_m = moves[moved]
    x_c = x_c + x_m
    y_c = y_c + y_m
    if -calcDistance([x_c, y_c], end) < 0 and solution_fitness == 0:
        route.append([x_c, y_c])
    else:
        break

#podsumowanie:
print("Parameters of the best solution : \n {solution} (in {number_of_moves} moves)".format(solution=solution[:number_of_moves],
                                                                                number_of_moves=number_of_moves))
print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=
                                                                       solution_fitness))
print("Number of generations passed is {generations_completed}".format(generations_completed=
                                                                       ga_instance.generations_completed))
# przygotuj szkielet
fig = plt.figure()
data = img
im = plt.imshow(data, cmap="gray", vmin=0, vmax=3)


# stan początkowy to lairynt bez drogi
def init():
    im.set_data(data)


# animacja aktualizująca drogę
def animate(i):
    # wykonuj tylko jeżeli są dostępne ruchy
    if i < len(route):
        data[route[i][0], route[i][1]] = 3
    im.set_data(data)
    return im


# Uruchumioenie animacji
anim = animation.FuncAnimation(fig, animate, init_func=init, frames=30,
                               interval=100)
plt.show()

#wyswietlenie wykresu: jak zmieniala sie ocena na przestrzeni pokolen
ga_instance.plot_fitness()
