import numpy as np
import unittest
from numpy.testing import assert_array_almost_equal
import os, sys
from openpyxl import load_workbook
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from packages import resistance, fctAnnexes

path = os.getcwd()
pathdir = os.path.dirname(path)
workbookDVP = load_workbook(filename=os.path.join(pathdir,"data/Devis_masse.xlsx"), data_only=True)

class testModule_resistance(unittest.TestCase):
    def testEfforts_resistance(self):
        Vs = fctAnnexes.nds2ms(4)
        Lambda = np.deg2rad(0)
        assert_array_almost_equal(round(resistance.efforts_resistance(Vs, Lambda, workbookDVP)[0][0],2), -31.83)

        Vs = fctAnnexes.nds2ms(-4)
        assert_array_almost_equal(round(resistance.efforts_resistance(Vs, Lambda, workbookDVP)[0][0],2), -199999.95)



if __name__=="__main__":
    unittest.main()