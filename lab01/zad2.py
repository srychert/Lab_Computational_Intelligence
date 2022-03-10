import math
import random


def my_print(obj, depth):
    if len(obj) > depth:
        print(f"{str(obj[:depth])[:-1]}, ... , {obj[-1]}]")
    else:
        print(obj)


vector1 = [3, 8, 9, 10, 12]
vector2 = [8, 7, 7, 5, 6]


# a)
def sum_vectors(v1, v2):
    v_sum = []
    for i in range(min(len(v1), len(v2))):
        v_sum.append(v1[i]+v2[i])
    return v_sum


print(f"suma wektorów: {sum_vectors(vector1, vector2)}")


def multiply_vectors(v1, v2):
    v_mult = []
    for i in range(min(len(v1), len(v2))):
        v_mult.append(v1[i]*v2[i])
    return v_mult


print(f"iloczyn wektorów: {multiply_vectors(vector1, vector2)}")


# b)
def iloczyn_skalarny(v1, v2):
    result = 0
    for i in range(min(len(v1), len(v2))):
        result += v1[i] * v2[i]
    return result


print(f"iloczyn skalarny: {iloczyn_skalarny(vector1, vector2)}")


# c)
def vector_length(v):
    sum_squared = 0
    for i in v:
        sum_squared += i**2
    return math.sqrt(sum_squared)


print(
    f"długości euklidesowe: {vector_length(vector1), vector_length(vector2)}")


# d)
vector_random = []
for ele in range(50):
    vector_random.append(random.randint(1, 100))

print("=================================")
print("Losowy wektor z zakresu [1, 100]:")
my_print(vector_random, 10)


# e)
def vector_mean(v):
    result = 0
    for i in v:
        result += i
    return result/len(v)


def standard_deviation(v):
    mean = vector_mean(v)
    variance_sum = 0
    for i in v:
        variance_sum += (i - mean)**2
    return math.sqrt(variance_sum/len(v))


print(f"średnia: {vector_mean(vector_random)}")
print(f"minimum: {min(vector_random)}")
print(f"maximum: {max(vector_random)}")
print(f"odchylenie standardowe: {standard_deviation(vector_random)}")


# f)
def vector_normalize(v):
    new_vector = []
    v_min = min(v)
    v_max = max(v)
    for i in v:
        new_ele = (i - v_min) / (v_max - v_min)
        new_vector.append(new_ele)
    return new_vector


normalized_vector = vector_normalize(vector_random)
print("=================================")
print("Wektor znormalizowany:")
my_print(normalized_vector, 10)
print(
    f"dawny max: {max(vector_random)} na pozycji {vector_random.index(max(vector_random))}"
    f"\nnowa wartość na tej pozycji: {normalized_vector[vector_random.index(max(vector_random))]}")


# g)
def vector_standardize(v):
    new_vector = []
    mean = vector_mean(v)
    devi = standard_deviation(v)
    for i in v:
        new_ele = (i - mean) / devi
        new_vector.append(new_ele)
    return new_vector


print("=================================")
print("Wektor ustandaryzowany:")
standardized_vector = vector_standardize(vector_random)
my_print(standardized_vector, 10)
print(f"Nowa średnia: {vector_mean(standardized_vector)}")
print(f"Nowe odchylenie std: {standard_deviation(standardized_vector)}")


# h)
def vector_discretization(v, start=0, stop=100, step=10):
    new_vector = []
    for e in v:
        for i in range(start, stop, step):
            right_end = i + step-1
            symbol = f"{right_end+1})"
            if(i == stop-step):
                right_end = i + step
                symbol = f"{right_end}]"
            if right_end > e >= i:
                new_vector.append(f"[{i}, {symbol}")
    return new_vector


print("=================================")
print("Wektor po dyskretyzacji:")
my_print(vector_discretization(vector_random), 10)
