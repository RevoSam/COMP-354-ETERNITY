# unit tests for all functions

import unittest
from gamma import *

class Test_Gamma(unittest.TestCase):

    def test_gamma_valid_input(self):
        self.assertEqual(round(gamma(0.5), 10), 1.7724538509)
        self.assertEqual(round(gamma(1), 10), 1)
        self.assertEqual(round(gamma(2), 10), 1)
        self.assertEqual(round(gamma(5), 10), 24)
    
    def test_gamma_invalid_input(self):
        self.assertEqual(gamma(0), None)

if __name__ == '__main__':
    unittest.main()