import math
import random

vector1 = [3, 8, 9, 10, 12]
vector2 = [8, 7, 7, 5, 6]


# a)
def sum_vectors(v1, v2):
    v_sum = []
    for i in range(min(len(v1), len(v2))):
        v_sum.append(v1[i]+v2[i])
    return v_sum


print(sum_vectors(vector1, vector2))


def multiply_vectors(v1, v2):
    v_mult = []
    for i in range(min(len(v1), len(v2))):
        v_mult.append(v1[i]*v2[i])
    return v_mult


print(multiply_vectors(vector1, vector2))


# b)
def iloczyn_skalarny(v1, v2):
    result = 0
    for i in range(min(len(v1), len(v2))):
        result += v1[i] * v2[i]
    return result


print(iloczyn_skalarny(vector1, vector2))


# c)
def vector_length(v):
    sum_squared = 0
    for i in v:
        sum_squared += i**2
    return math.sqrt(sum_squared)


print(vector_length(vector1))
print(vector_length(vector2))


# d)
vector_random = []
for ele in range(50):
    vector_random.append(random.randint(1, 100))
print(vector_random)


# e)
def v_mean(v):
    result = 0
    for i in v:
        result += i
    return result/len(v)


def standard_deviation(v):
    mean = v_mean(v)
    variance_sum = 0
    for i in v:
        variance_sum += (i - mean)**2
    return math.sqrt(variance_sum/len(v))


print(v_mean(vector_random))
print(min(vector_random))
print(max(vector_random))
print(standard_deviation(vector_random))


# f)
def vector_normalize(v):
    new_vector = []
    v_min = min(v)
    v_max = max(v)
    for i in range(len(v)):
        new_ele = (v[i] - v_min) / (v_max - v_min)
        new_vector.append(new_ele)
    return new_vector


print(vector_normalize(vector_random))

# g) Dokończ
