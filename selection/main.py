import time
import unittest

import numpy as np
import pandas as pd

FILE = 'sample'
# FILE = 'me_at_the_zoo'
# FILE = 'videos_worth_spreading'
# FILE = 'trending_today'
# FILE = 'kittens'
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

    return V, E, R, C, X, gain, ep_vid, cache_ep, caches, vids


def output(results, outfile='truc')
    outfile += '.out'
    with open(outfile, 'w') as f:
        f.write(str(len(results)) + '\n')
        for k, vids in results.items():
            f.write(str(k) + ' ' + ' '.join(str(v) for v in vids) + '\n')


def choose_vid(gain, ep_vid, cache_ep, caches, vids):

    # find corresponding cache video
    cache, vid = np.argmax(gain)
    results[cache].append(vid)

    





#
# LAUNCHING
#
if __name__ == '__main__':
    # unittest.main()

    begin = time.time()
    V, E, R, C, X, gain, ep_vid, cache_ep, caches, vids = parse(FILENAME)
    end = time.time()
    print(end - begin)
    # print('V', V)
    # print('E', E)
    # print('R', R)
    # print('C', C)
    # print('X', X)
    # print('gain\n', gain)
    # print('ep_vid\n', ep_vid)
    # print('cache_ep\n', cache_ep)
    # print('caches\n', caches)
    # print('vids\n', vids)
