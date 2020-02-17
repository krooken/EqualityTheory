""" Generates a random CNF file """

import random

k = 3
n = 170
m = int(n * 4.26)

random.seed()  # Uses system time
for nc in range(0, m):
    c = []
    while len(c) < k:
        lit = (random.randint(1, n)) * (1 if random.randint(0, 1) else -1)
        if lit not in c and -lit not in c:
            c.append(lit)
    for lit in c:
        print(str(lit) + " ")  # , end="")
    print("0")
