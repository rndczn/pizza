"""Main for hashcode test."""

import random

import numpy as np

FILE = 'data/big.in'
DIRECTIONS = ['LEFT', 'RIGHT', 'UP', 'DOWN']


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

    M = 0
    T = 1

    def __init__(self, R, C, L, H, tm):
        self.R = R
        self.C = C
        self.L = L
        self.H = H
        self.tm = tm  # tableau avec les tomates et mushrooms
        self.mask = np.zeros((R, C))  # tableau gardant toutes les slices prises
        self.slices = []
        self.smaller = self.M if 2 * np.sum(self.tm) > self.R * self.C else self.T

    @property
    def score(self):
        return np.sum(self.mask)

    @property
    def nb_smaller(self):
        return np.sum(self.tm) if self.smaller == self.T else self.R * self.C - np.sum(self.tm)

    def create_or_update(self, old_slice, new_slice):
        # replace old slice by new slice
        if old_slice is not None:
            for n, s in enumerate(self.slices):
                # same object, should work :D YOLO
                if s == old_slice:
                    self.slices[n] = new_slice
        else:
            self.slices.append(new_slice)

        self.mask[new_slice.r1:new_slice.r2+1, new_slice.c1:new_slice.c2+1] = 1

    def grow(self, slic):
        potential_slices = []

        for d in DIRECTIONS:
            s = slic.extend(d)
            if s is not None:
                potential_slices.append(s)

        if potential_slices:
            new_slice = self.choose_best_slice(potential_slices)
            self.create_or_update(slic, new_slice)
            return True

        elif not slic.is_valid:
            self.delete(slic)

        return False

    def choose_best_slice(self, potential_slices):
        potential_slices.sort(key=lambda x: abs(x.nb_of_smaller - self.L))
        return potential_slices[0]

    def delete(self, slic):
        self.slices.remove(slic)
        for r in range(slic.r1, slic.r2 + 1):
            for c in range(slic.c1, slic.c2 + 1):
                self.mask[r, c] = 0

    def grow_invalid(self):
        priority = [x for x in self.slices if not x.is_valid]
        # si jms aucune ne grandit -> False
        return any([self.grow(s) for s in priority])

    def grow_valid(self):
        # si jms aucune ne grandit -> False
        return any([self.grow(s) for s in self.slices])

    def initial_positions(self):
        nb_initial_positions = self.nb_smaller // self.L
        while len(self.slices) != nb_initial_positions:
            position = (random.randrange(self.R), random.randrange(self.C))
            if self.mask[position] != 1 and self.tm[position] == self.smaller:
                self.create_or_update(None, Slice(*position, *position, self))


class Slice(object):

    TOO_BIG = False
    TOO_FEW_M = False
    TOO_FEW_T = False
    ALREADY_TAKEN = False
    GROW_WONT_HELP = False

    def __init__(self, r1, c1, r2, c2, pizza):
        self.r1 = min(r1, r2)
        self.c1 = min(c1, c2)
        self.r2 = max(r1, r2)
        self.c2 = max(c1, c2)
        self.pizza = pizza

    def __repr__(self):
        return '{r1} {c1} {r2} {c2}'.format(**self.__dict__)

    @property
    def size(self):
        return (abs(self.r2 - self.r1) + 1) * (abs(self.c1 - self.c2) + 1)

    @property
    def total_t(self):
        return np.sum(self.pizza.tm[self.r1:self.r2+1, self.c1:self.c2+1])

    @property
    def total_m(self):
        return self.size - self.total_t

    @property
    def ratio_t_m(self):
        return self.total_t / self.total_m

    @property
    def nb_of_smaller(self):
        return self.total_t if self.pizza.smaller == self.pizza.T else self.total_m

    @property
    def is_not_doomed(self):
        # too big or could not grow to a valid slice
        H, L = self.pizza.H, self.pizza.L
        r1, c1, r2, c2 = self.r1, self.c1, self.r2, self.c2

        size = self.size
        total_t = self.total_t

        if size > H:
            return self.TOO_BIG

        if H - size < L - min(total_t, size - total_t):
            return self.GROW_WONT_HELP

        return True

    @property
    def is_valid(self):
        H, L = self.pizza.H, self.pizza.L
        r1, c1, r2, c2 = self.r1, self.c1, self.r2, self.c2

        size = self.size
        total_t = self.total_t

        if size > H:
            return self.TOO_BIG

        if total_t < L:
            return self.TOO_FEW_T

        if size - total_t < L:
            return self.TOO_FEW_M

        # if np.sum(self.pizza.mask[r1:r2+1, c1:c2+1]) != 0:
        #     return self.ALREADY_TAKEN

        return True

    def extend(self, direction):
        s = Slice(**self.__dict__)

        if direction == 'LEFT':
            if self.c1 == 0:
                return None
            if any([self.pizza.mask[i, self.c1 - 1] == 1 for i in range(self.r1, self.r2 + 1)]):
                return None
            s.c1 -= 1

        if direction == 'RIGHT':
            if self.c2 == self.pizza.C - 1:
                return None
            if any([self.pizza.mask[i, self.c2 + 1] == 1 for i in range(self.r1, self.r2 + 1)]):
                return None
            s.c2 += 1

        if direction == 'UP':
            if self.r1 == 0:
                return None
            if any([self.pizza.mask[self.r1 - 1, i] == 1 for i in range(self.c1, self.c2 + 1)]):
                return None
            s.r1 -= 1

        if direction == 'DOWN':
            if self.r2 == self.pizza.R - 1:
                return None
            if any([self.pizza.mask[self.r2 + 1, i] == 1 for i in range(self.c1, self.c2 + 1)]):
                return None
            s.r2 += 1

        if s.is_not_doomed:
            return s
        return None


if __name__ == '__main__':
    pizza = Pizza(*parse(FILE))
    print('R        ', pizza.R)
    print('C        ', pizza.C)
    print('L        ', pizza.L)
    print('H        ', pizza.H)
    print('smaller  ', 'T' if pizza.smaller == pizza.T else 'M')
    print('nbsmaller', pizza.nb_smaller)
    print('pizza\n', pizza.tm)
    # print('slice 0,0,2,4:', Slice(0, 0, 2, 4, pizza))

    # print()
    # print('#' * 10)
    # print('VALID SLICE')
    # print('TOO_BIG      ' + ' ' * 10,
    #       Slice.TOO_BIG   == Slice(0, 0, 2, 4, pizza).is_valid)
    # print('TOO_FEW_M    ' + ' ' * 10,
    #       Slice.TOO_FEW_M == Slice(0, 0, 2, 0, pizza).is_valid)
    # print('TOO_FEW_T    ' + ' ' * 10,
    #       Slice.TOO_FEW_T == Slice(1, 1, 1, 3, pizza).is_valid)
    # pizza.mask[0,0] = 1
    # print('ALREADY_TAKEN' + ' ' * 10,
    #       Slice.ALREADY_TAKEN == Slice(0, 0, 2, 1, pizza).is_valid)
    # pizza.mask[0,0] = 0
    # print('VALID        ' + ' ' * 10,
    #       Slice(0, 0, 2, 1, pizza).is_valid)



    # print()
    # print('#' * 10)
    # print('EXTEND')
    # s = Slice(0, 0, 0, 0, pizza)
    # pizza.create_or_update(None, s)
    # print('Sliced added', pizza.mask[0,0] == 1,
    #                       pizza.mask[0,1] == 0,
    #                       pizza.mask[1,0] == 0)
    # print('slices      ', pizza.slices)
    # print('mask      \n', pizza.mask)
    # new_s = s.extend('DOWN')
    # print('ADDING NEW S')
    # print('new_s       ', new_s)
    # pizza.create_or_update(s, new_s)
    # print('slices      ', pizza.slices)
    # print('mask      \n', pizza.mask)

    # s2 = Slice(0, 0, 0, 0, pizza)
    # pizza.create_or_update(None, s)
    # print('slices      ', pizza.slices)
    # print('mask      \n', pizza.mask)


    # s = Slice(0, 0, 2, 1, pizza)
    # print(s.is_valid)

    from datetime import datetime as dt
    print(dt.now())
    pizza.initial_positions()
    
    # print()
    # print('#' * 10)
    # print('INITIAL')
    # print('#' * 10)
    # print(pizza.mask)
    # print()
    
    i = 0
    while pizza.grow_invalid():
        # print()
        # print('#' * 10)
        # print('# ' + str(i))
        # print('#' * 10)
        # print(i, pizza.score)
        i += 1
        # print(pizza.mask)
        pass

    while pizza.grow_valid():
        # print()
        # print('#' * 10)
        # print('# ' + str(i))
        # print('#' * 10)
        # print(i, pizza.score)
        # i += 1
        # print(pizza.mask)
        pass

    # print()
    # print('#' * 10)
    # print('# END')
    # print('#' * 10)
    print(dt.now())
    print(pizza.score)
    # print(pizza.slices)
    # print(pizza.mask)
