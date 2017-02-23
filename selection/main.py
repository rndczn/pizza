import time
import unittest

from collections import defaultdict
from datetime import datetime as dt

import numpy as np
import pandas as pd

FILE = 'sample'
FILE = 'me_at_the_zoo'
FILE = 'videos_worth_spreading'
FILE = 'trending_today'
FILE = 'kittens'

def parse(file):
    filename = 'data/' + file + '.in'
    with open(filename) as f:
        V, E, R, C, X = map(int, f.readline().split())
        gain = np.zeros((C, V), dtype=np.int)
        ep_vid = np.zeros((E, V), dtype=np.int)
        cache_ep = np.zeros((C, E), dtype=np.int)
        caches = X * np.ones(C, dtype=np.int)
        vids = np.array(list(map(int, f.readline().split())))

        for ep in range(E):
            Ld, K = list(map(int, f.readline().split()))
            for _ in range(K):
                c, Lc = list(map(int, f.readline().split()))
                cache_ep[c,ep] = Ld - Lc

        for _ in range(R):
            Rv, Re, Rn = list(map(int, f.readline().split()))
            ep_vid[Re,Rv] = Rn

        begin = time.time()
        gain = np.dot(cache_ep, ep_vid)
        end = time.time()
        print('dot took', end - begin)

        mask = np.ones((C,V), dtype=np.int)
        for c in range(C):
            for v in range(V):
                if vids[v] > caches[c]:
                    mask[c,v] = 0

    return V, E, R, C, X, gain, ep_vid, cache_ep, caches, vids, mask


def output(results, outfile='truc'):
    outfile = 'data/' + outfile + '.out'
    with open(outfile, 'w') as f:
        f.write(str(len(results)) + '\n')
        for k, vids in results.items():
            f.write(str(k) + ' ' + ' '.join(str(v) for v in vids) + '\n')


def choose_vid(gain, ep_vid, cache_ep, caches, vids, results, i, mask):

    from numpy import unravel_index
    cache, vid = unravel_index(gain.argmax(), gain.shape)
    if gain[cache, vid] == 0:
        return

    results[cache].append(vid)
    caches[cache] -= vids[vid]

    eps = [ep for ep in range(cache_ep.shape[1]) if cache_ep[cache, ep] > 0]
    for ep in eps:
        linked_caches = [cach for cach in range(cache_ep.shape[0])
                              if cache_ep[cach,ep] != 0 and cach != cache]
        for cc in linked_caches:
            gain[cc,vid] -= ep_vid[ep,vid] * cache_ep[cc,ep]

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

    begin = time.time()
    for file in ['sample', 'me_at_the_zoo', 'videos_worth_spreading',
                 'trending_today', 'kittens']:
        print('start ' + file + ' ' + ' {:%Hh%Mm%S}'.format(dt.now()))
        V, E, R, C, X, gain, ep_vid, cache_ep, caches, vids, mask = parse(file)
        run(gain, ep_vid, cache_ep, caches, vids, file, mask)
        print('end ' + file)
    end = time.time()
    print(end - begin)
