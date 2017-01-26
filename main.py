"""Main for hashcode test."""

import numpy as np

FILE = 'data/example.in'

def parse(file):
    with open(file) as f:
        for i, line in enumerate(f):
            if i == 0:
                R, C, L, H = (int(el) for el in line.split())
                pizza = np.zeros((R, C))
                continue
            for j in range(C):
                # T = 1, M = 0
                pizza[i-1, j] = (line[j] == 'T')
    return R, C, L, H, pizza


if __name__ == '__main__':
    R, C, L, H, pizza = parse(FILE)
    print('R', R)
    print('C', C)
    print('L', L)
    print('H', H)
    print('pizza', pizza)
