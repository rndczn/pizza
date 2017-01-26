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


class Pizza(object):

    def __init__(self, R, C, L, H, pizza):
        self.R = R
        self.C = C
        self.L = L
        self.H = H
        self.pizza = pizza
        self.mask = np.zeros((R, C))
        self.slices = []


class Slice(object):

    TOO_BIG = 2
    TOO_FEW_M = 3
    TOO_FEW_T = 4
    ALREADY_TAKEN = 4

    def __init__(self, r1, c1, r2, c2):
        self.r1 = r1
        self.c1 = c1
        self.r2 = r2
        self.c2 = c2

    @property
    def size(self):
        return (abs(self.r2 - self.r1) + 1) * (abs(self.c1 - self.c2) + 1)

    def total_t(self, pizza):
        return np.sum(pizza.pizza[min(self.r1,self.r2):max(self.r1,self.r2)+1, 
                                  min(self.c1,self.c2):max(self.c1,self.c2)+1])

    def total_m(self, pizza):
        return self.size - self.total_t(pizza)

    def ratio_t_m(self, pizza):
        return self.total_t(pizza) / self.size

    def is_valid(self, pizza):
        H, L = pizza.H, pizza.L

        r1, c1, r2, c2 = self.r1, self.c1, self.r2, self.c2
        size = self.size
        total_t = self.total_t(pizza)

        if size > H:
            return self.TOO_BIG

        if total_t < L:
            return self.TOO_FEW_T

        if size - total_t < L:
            return self.TOO_FEW_M

        if np.sum(pizza.mask[min(r1,r2):max(r1,r2)+1, min(c1,c2):max(c1,c2)+1]) != 0:
            return self.ALREADY_TAKEN

        return True


if __name__ == '__main__':
    pizza = Pizza(*parse(FILE))
    print('R', pizza.R)
    print('C', pizza.C)
    print('L', pizza.L)
    print('H', pizza.H)
    print('pizza\n', pizza.pizza)
    print('TOO_BIG      ', Slice.TOO_BIG   == Slice(0, 0, 2, 4).is_slice_valid(pizza))
    print('TOO_FEW_M    ', Slice.TOO_FEW_M == Slice(0, 0, 2, 0).is_slice_valid(pizza))
    print('TOO_FEW_T    ', Slice.TOO_FEW_T == Slice(1, 1, 1, 3).is_slice_valid(pizza))
    pizza.mask[0,0] = 1
    print('ALREADY_TAKEN', Slice.ALREADY_TAKEN == Slice(0, 0, 2, 1).is_slice_valid(pizza))
    pizza.mask[0,0] = 0
    print('VALID        ', Slice(0, 0, 2, 1).is_slice_valid(pizza))

