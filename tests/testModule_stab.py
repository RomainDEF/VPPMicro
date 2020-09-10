from Module_stab import *
import unittest
from numpy.testing import assert_array_almost_equal
from fonctions_annexes import *
import random

class testModule_stab(unittest.TestCase):
    def testEfforts_hydrostat(self):
        DELTA = 72
        phi = np.deg2rad(15)
        theta = np.deg2rad(0)
        assert_array_almost_equal(efforts_hydrostat(phi, theta, DELTA), np.array([[0, -0.0711*DELTA*9.81],[0,0],[0,0]]))

        DELTA = 72
        phi = np.deg2rad(72.5)
        theta = np.deg2rad(0)
        assert_array_almost_equal(efforts_hydrostat(phi, theta, DELTA),
                                  np.array([[0, -0.28615 * DELTA * 9.81], [0, 0], [0, 0]]))

        DELTA = 72
        phi = np.deg2rad(-72.5)
        theta = np.deg2rad(0)
        assert_array_almost_equal(efforts_hydrostat(-phi, theta, DELTA), -efforts_hydrostat(phi, theta, DELTA))

        DELTA = 72
        phi = np.deg2rad(0)
        theta = np.deg2rad(2.5)
        assert_array_almost_equal(efforts_hydrostat(phi, theta, DELTA), np.array([[0, 0], [0, -8.325 * DELTA * 9.81], [0, 0]]))

        DELTA = 72
        phi = np.deg2rad(0)
        theta = np.deg2rad(5.5)
        assert_array_almost_equal(-efforts_hydrostat(phi, theta, DELTA), efforts_hydrostat(phi, -theta, DELTA))

if __name__=="__main__":
    unittest.main()