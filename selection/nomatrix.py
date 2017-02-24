import time
import unittest
import sys

from collections import defaultdict
from datetime import datetime as dt

import numpy as np
from numpy import unravel_index
from numpy.random import choice
import pandas as pd

FILE = 'sample'
FILE = 'me_at_the_zoo'
FILE = 'videos_worth_spreading'
FILE = 'trending_today'
FILE = 'kittens'


class Cache():
    def __init__(self, capacity):
        self.capacity = capacity
        self.videos_gain = {}
        self.max_gain = []

class Endpoint():
    def __init__(self, lat):
        self.caches = {}
        self.requests = {}
        self.lat = lat

    def add_req(self, vid, n):
        pass

def parse(file):
    filename = 'data/' + file + '.in'
    with open(filename) as f:
        V, E, R, C, X = map(int, f.readline().split())

        caches = [Cache(X) for _ in range(C)]
        vids = [int(i) for i in f.readline().split()]

        endpoints = []
        for _ in range(E):
            LAT, n_c = map(int, f.readline().split())
            ep = Endpoint(LAT)
            for _ in range(n_c):
                cache, lat = map(int, f.readline().split())
                ep.caches[cache] = lat
            endpoints.append(ep)

        for _ in range(R):
            vid, ep, n = map(int, f.readline().split())
            endpoints[ep].add_req(vid, n)

    return V, E, R, C, X, gain, ep_vid, cache_ep, caches, vids, mask


def output(results, outfile='truc'):
    outfile = 'data/' + outfile + '.out'
    with open(outfile, 'w') as f:
        f.write(str(len(results)) + '\n')
        for k, vids in results.items():
            f.write(str(k) + ' ' + ' '.join(str(v) for v in vids) + '\n')


def choose_vid(gain, ep_vid, cache_ep, caches, vids, results, i, mask):
    cache, vid = unravel_index(gain.argmax(), gain.shape)
    cache, vid = unravel_index(choice(ravel(gain).argsort()[-2:]), gain.shape)
    if gain[cache, vid] == 0:
        return

    results[cache].append(vid)
    caches[cache] -= vids[vid]

    eps = [ep for ep in range(cache_ep.shape[1]) if cache_ep[cache, ep] > 0]
    for ep in eps:
        linked_caches = [cach for cach in range(cache_ep.shape[0])
                         if cache_ep[cach, ep] != 0 and cach != cache]
        for cc in linked_caches:
            gain[cc, vid] -= ep_vid[ep, vid] * cache_ep[cc, ep]

    gain[cache, vid] = 0
    for i, v in enumerate(vids):
        if v > caches[cache]:
            gain[cache, i] = 0

    return gain


def run(gain, ep_vid, cache_ep, caches, vids, filename, mask):
    results = defaultdict(list)
    i = 0
    new_gain = choose_vid(gain, ep_vid, cache_ep, caches, vids, results, i, mask)
    while new_gain is not None:
        i += 1
        if i % 100 == 0:
            output(results, filename)
        new_gain = choose_vid(new_gain, ep_vid, cache_ep, caches, vids, results, i, mask)
    output(results, filename)


#
# LAUNCHING
#
if __name__ == '__main__':
    # unittest.main()

    file = sys.argv[1]

    begin = time.time()
    print('start ' + file + ' ' + ' {:%Hh%Mm%S}'.format(dt.now()))
    V, E, R, C, X, gain, ep_vid, cache_ep, caches, vids, mask = parse(file)
    run(gain, ep_vid, cache_ep, caches, vids, file, mask)
    print('end ' + file)
    end = time.time()
    print(end - begin)
