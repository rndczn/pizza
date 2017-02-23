import time
import unittest

from collections import defaultdict

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

        gain = np.dot(cache_ep, ep_vid)

        for c in range(C):
            for v in range(V):
                if vids[v] > caches[c]:
                    gain[c,v] = 0

    return V, E, R, C, X, gain, ep_vid, cache_ep, caches, vids


def output(results, outfile='truc'):
    outfile = 'data/' + outfile + '.out'
    with open(outfile, 'w') as f:
        f.write(str(len(results)) + '\n')
        for k, vids in results.items():
            f.write(str(k) + ' ' + ' '.join(str(v) for v in vids) + '\n')


def choose_vid(gain, ep_vid, cache_ep, caches, vids, results, i):

    from numpy import unravel_index
    cache, vid = unravel_index(gain.argmax(), gain.shape)
    if gain[cache, vid] == 0:
        return

    results[cache].append(vid)
    caches[cache] -= vids[vid]

    for ep in [ep for ep in range(cache_ep.shape[1]) if cache_ep[cache, ep] > 0]:
        ep_vid[ep,vid] = 0

    new_gain = np.dot(cache_ep, ep_vid)

    new_gain[cache, vid] = 0
    for c in range(C):
        for v in range(V):
            if c in results.keys():
                if v in results[c]:
                    new_gain[c,v] = 0
            if vids[v] > caches[c]:
                new_gain[c,v] = 0

    return new_gain

def run(gain, ep_vid, cache_ep, caches, vids, filename):
    results = defaultdict(list)
    i = 0
    new_gain = choose_vid(gain, ep_vid, cache_ep, caches, vids, results, i)
    while new_gain is not None:
        i += 1
        new_gain = choose_vid(new_gain, ep_vid, cache_ep, caches, vids, results, i)
    output(results, filename)

#
# LAUNCHING
#
if __name__ == '__main__':
    # unittest.main()

    begin = time.time()
    for file in ['sample', 'me_at_the_zoo', 'videos_worth_spreading',
                 'trending_today', 'kittens']:
        print('start ' + file)
        run(gain, ep_vid, cache_ep, caches, vids, FILE)
        print('end ' + file)
    end = time.time()
    print(end - begin)
