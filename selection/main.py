import unittest

import numpy as np
import pandas as pd

FILE = 'sample'
# FILE = 'kittens'
# FILE = 'me_at_the_zoo'
# FILE = 'trending_today'
# FILE = 'videos_worth_spreading'
FILENAME = 'data/' + FILE + '.in'

def parse(filename):
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
        ep_vid[ep_vid != 0] = 1
        cache_ep[cache_ep != 0] = 1

    return V, E, R, C, X, gain, ep_vid, cache_ep, caches, vids


#
# LAUNCHING
#
if __name__ == '__main__':
    # unittest.main()
    V, E, R, C, X, gain, ep_vid, cache_ep, caches, vids = parse(FILENAME)
    print('V', V)
    print('E', E)
    print('R', R)
    print('C', C)
    print('X', X)
    print('gain\n', gain)
    print('ep_vid\n', ep_vid)
    print('cache_ep\n', cache_ep)
    print('caches\n', caches)
    print('vids\n', vids)
