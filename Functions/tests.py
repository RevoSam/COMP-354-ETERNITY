# unit tests for all functions

import unittest
from special_fn import *
from subordinate_fn import PI

class Test_Gamma(unittest.TestCase):

    def test_gamma_valid_input(self):
        self.assertAlmostEqual(gamma(0.1), 9.513507699)
        self.assertAlmostEqual(gamma(0.2), 4.590843712)
        self.assertAlmostEqual(gamma(0.5), 1.772453851)
        self.assertAlmostEqual(gamma(1), 1)
        self.assertAlmostEqual(gamma(2), 1)
        self.assertAlmostEqual(gamma(5), 24)
    
    def test_gamma_invalid_input(self):
        with self.assertRaises(ValueError):
            gamma(0)
        with self.assertRaises(ValueError):
            gamma(-1)

class Test_SD(unittest.TestCase):

    def test_sd_ints(self):
        self.assertAlmostEqual(standard_deviation([12, 11, 17, 15, 13, 12, 14, 15], True), 1.9955307207)
        self.assertAlmostEqual(standard_deviation([12, 11, 17, 15, 13, 12, 14, 15], False), 1.8666480654)
        
    def test_sd_floats(self):
        self.assertAlmostEqual(standard_deviation([2.5, 3.4, 2.1, 3.1, 3.2, 2.9], True), 0.4844240567)
        self.assertAlmostEqual(standard_deviation([2.5, 3.4, 2.1, 3.1, 3.2, 2.9], False), 0.4422166387)

    def test_sd_mixed(self):
        self.assertAlmostEqual(standard_deviation([7, 6.5, 7.5, 6, 3, 5.6], True), 1.5895492023)
        self.assertAlmostEqual(standard_deviation([7, 6.5, 7.5, 6, 3, 5.6], False), 1.4510532573)

class Test_MAD(unittest.TestCase):

    def test_mad_ints(self):
        self.assertAlmostEqual(mad([12, 11, 17, 15, 13, 12, 14, 15]), 1.625)
        
    def test_mad_floats(self):
        self.assertAlmostEqual(mad([2.5, 3.4, 2.1, 3.1, 3.2, 2.9]), 0.3777777778)

    def test_mad_mixed(self):
        self.assertAlmostEqual(mad([7, 6.5, 7.5, 6, 3, 5.6]), 1.0888888889)

class Test_Natural_Exp(unittest.TestCase):

    def test_natural_exp_(self):
        self.assertAlmostEqual(natural_exp(2, 3, 4), 162)
        self.assertAlmostEqual(natural_exp(100, 1.1, 4), 146.41)
        self.assertAlmostEqual(natural_exp(-100, 0.5, -10), -102400)

class Test_Sinh(unittest.TestCase):

    def test_sinh(self):
        self.assertAlmostEqual(sinh(0), 0)
        self.assertAlmostEqual(sinh(1), 1.1752011936)
        self.assertAlmostEqual(sinh(PI), 11.5487393573)

class Test_Power(unittest.TestCase):

    def test_power(self):
        self.assertAlmostEqual(power(2, 10), 1024)
        self.assertAlmostEqual(power(2, 2.5), 5.6568542495)
        self.assertAlmostEqual(power(2.5, 2), 6.25)
        self.assertAlmostEqual(power(2.5, 2.5), 9.8821176880)

class Test_Arccos(unittest.TestCase):

    def test_arccos_valid_input(self):
        self.assertAlmostEqual(arccos(1), 0)
        self.assertAlmostEqual(arccos(-1), 3.1415926536)
        self.assertAlmostEqual(arccos(0.5), 1.0471974888)
        self.assertAlmostEqual(arccos(0.1), 1.4706289917)

    def test_arccos_invalid_input(self):
        with self.assertRaises(ValueError):
            arccos(5)
        with self.assertRaises(ValueError):
            arccos(-2)
            
if __name__ == '__main__':
    unittest.main()