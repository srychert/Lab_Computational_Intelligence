import math


def prime(n):
    for i in range(2, n):
        if n % i == 0:
            return False
    return True


print(prime(3))
print(prime(4))
print(prime(49))
