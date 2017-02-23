import unittest

import numpy as np
import pandas as pd

FILE = ''


#
# CODE
#
def parse(filename):
    with open(filename) as f:
        pass



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
    unittest.main()
