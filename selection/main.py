import unittest

import numpy as np
import pandas as pd

FILE = 'sample'
# FILE = 'kittens'
# FILE = 'me_at_the_zoo'
# FILE = 'trending_today'
# FILE = 'videos_worth_spreading'
FILENAME = 'data/' + FILE + '.in'

#
# CODE
#
def parse(filename):
    with open(filename) as f:
        V, E, R, C, X = map(int, f.readline().split())
        endpoints = []
        caches = []

        vids = list(map(int, f.readline().split()))

        for _ in range(E):
            Ld, K = list(map(int, f.readline().split()))
            endpoint = EndPoint(Ld, K, R, C)
            for _ in range(K):
                c, Lc = list(map(int, f.readline().split()))
                endpoint.cache_servers_list[c] = Lc
                endpoint.cache_servers.append(c)
            endpoints.append(endpoint)

        for _ in range(R):
            Rv, Re, Rn = list(map(int, f.readline().split()))
            endpoints[Re].requests[Rv] = Rn


    return V, E, R, C, X, vids, endpoints, requests


class EndPoint(object):

    def __init__(self, Ld, K, R, C):
        self.Ld = Ld
        self.K = K
        self.cache_servers_list = [Ld] * C
        self.cache_servers = []
        self.requests = [0] * R

    def __repr__(self):
        return 'Ld:{Ld}/K:{K}/X:{X} => {cache_servers_list}'.format(**self.__dict__)


class Cache(object):

    def __init__(self, V):
        self.endpoints = []
        self.vids = [0] * V


#
# TESTS
#
class TestSelection(unittest.TestCase):

    def test_sample(self):
        """Example of test syntax."""
        self.assertEqual(1, 1)
        self.assertTrue(True)
        self.assertFalse(False)
        # be careful, None is considered false, prefer assertEqual to test
        # if result is false
        self.assertFalse(None)
        with self.assertRaises(Exception):
            raise Exception

    def setUp(self):
        """Define elements common to all tests."""
        self.common = 10


#
# LAUNCHING
#
if __name__ == '__main__':
    # unittest.main()
    V, E, R, C, X, vids, endpoints, requests = parse(FILENAME)
    print()
    print('V', V)
    print('E', E)
    print('R', R)
    print('C', C)
    print('X', X)
    print('vids', vids)
    print('endpoints', endpoints)
    print('requests', requests)
