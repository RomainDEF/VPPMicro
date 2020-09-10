import unittest
from numpy.testing import assert_array_almost_equal
import os, sys
from openpyxl import load_workbook
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from packages import fctAnnexes
from packages import aero
import random
import numpy as np

path = os.getcwd()
pathdir = os.path.dirname(path)

workbookAero = load_workbook(filename=os.path.join(pathdir,"data/Polaires_Voile_data4.xlsm"), data_only=True)

class testModule_aero(unittest.TestCase):
    def testPolaire_voile(self):
        rho_air = 1.225
        # Cas de test 1 : vent apparent inférieur à 1 noeud : pas de portance, pas de trainée
        Lambda = np.deg2rad(5)
        angle_allure = np.deg2rad(45)
        Vt = fctAnnexes.nds2ms(0.5)
        Vs = fctAnnexes.nds2ms(0)
        phi = 0
        torseur_aero_repVoile, CP_repVoile, deltav = aero.polaire_voile(Vt, Vs, rho_air, Lambda, angle_allure, phi, workbookAero)
        assert_array_almost_equal(torseur_aero_repVoile, np.zeros((3, 2)))
        assert_array_almost_equal(CP_repVoile, np.zeros((3, 1)))

        # Cas de test 2 : vent apparent égal à l'un des v_bateau du tableau excel
        Lambda = np.deg2rad(0)
        angle_allure = np.deg2rad(20)
        Vt = fctAnnexes.nds2ms(10)
        Vs = fctAnnexes.nds2ms(0)
        phi = 0
        torseur_aero_repVoile, CP_repVoile, deltav = aero.polaire_voile(Vt, Vs, rho_air, Lambda, angle_allure, phi, workbookAero)
        #Valeurs théoriques
        CP_repVoile_th = np.array([-0.047069719, 0, 1.151453695]).reshape(-1, 1)
        torseur_aero_repVoile_th = np.zeros((3, 2))
        Va = aero.vent_apparent(Vt, Vs, Lambda, angle_allure, phi)
        np.testing.assert_almost_equal(fctAnnexes.ms2nds(Va), 10, decimal=0)
        CL_th, CD_th = 0.621872556, 0.075411043
        S_th = 1.647
        L_th = 0.5 * rho_air * CL_th * S_th * Va ** 2
        D_th = 0.5 * rho_air * CD_th * S_th * Va ** 2
        torseur_aero_repVoile_th[0,0] = D_th
        torseur_aero_repVoile_th[1,0] = L_th
        #print("TEST________________________",torseur_aero_repVoile)
        assert_array_almost_equal(CP_repVoile_th, CP_repVoile,1)
        assert_array_almost_equal(torseur_aero_repVoile, torseur_aero_repVoile_th, 1)

        np.testing.assert_almost_equal(np.rad2deg(deltav), 8, 0)

    def testChgt_base_pt_application(self):
        # Cas de test 1 : angle de voile, gite et angle de dérive nuls
        CP_repVoile = np.array([0.03,0,1]).reshape(-1,1)
        O_repVoile_repBateau = np.array([0,0,0]).reshape(-1,1)
        deltav = 0
        Lambda = 0
        phi = 0
        CP_repAvBateau = aero.chgt_base_pt_application(CP_repVoile, O_repVoile_repBateau, deltav, Lambda, phi)
        assert_array_almost_equal(np.array([-0.03,0,1]).reshape(-1,1), CP_repAvBateau)

        # Cas de test 2 : Variation de l'angle de dérive, angle de la voile et angle de gîte nuls
        CP_repVoile = np.array([0.03, 0, 1]).reshape(-1, 1)
        O_repVoile_repBateau = np.array([0, 0, 0]).reshape(-1, 1)
        deltav = 0
        phi = 0
        Lambda1 = np.deg2rad(10)
        Lambda2 = np.deg2rad(-10)
        CP_repAvBateau1 = aero.chgt_base_pt_application(CP_repVoile, O_repVoile_repBateau, deltav, Lambda1, phi)
        CP_repAvBateau2 = aero.chgt_base_pt_application(CP_repVoile, O_repVoile_repBateau, deltav, Lambda2, phi)
        assert_array_almost_equal(CP_repAvBateau1, np.array([-0.03*np.cos(Lambda1),-0.03*np.sin(Lambda1),1]).reshape(-1,1))
        self.assertEqual(CP_repAvBateau1[0,0], CP_repAvBateau2[0,0])
        self.assertEqual(CP_repAvBateau1[1,0], -CP_repAvBateau2[1,0])
        self.assertEqual(CP_repAvBateau1[2,0], CP_repAvBateau2[2,0])

        # Cas de test 3 : Variation de l'angle de gite, angle de la voile et angle de dérive nuls
        CP_repVoile = np.array([0.03, 0, 1]).reshape(-1, 1)
        O_repVoile_repBateau = np.array([0, 0, 0]).reshape(-1, 1)
        deltav = 0
        phi1 = np.deg2rad(15)
        phi2 = np.deg2rad(-15)
        Lambda = 0
        CP_repAvBateau1 = aero.chgt_base_pt_application(CP_repVoile, O_repVoile_repBateau, deltav, Lambda, phi1)
        CP_repAvBateau2 = aero.chgt_base_pt_application(CP_repVoile, O_repVoile_repBateau, deltav, Lambda, phi2)
        assert_array_almost_equal(CP_repAvBateau1, np.array([-0.03, -np.sin(phi1), np.cos(phi1)]).reshape(-1, 1))
        self.assertEqual(CP_repAvBateau1[0, 0], CP_repAvBateau2[0, 0])
        self.assertEqual(CP_repAvBateau1[1, 0], -CP_repAvBateau2[1, 0])
        self.assertEqual(CP_repAvBateau1[2, 0], CP_repAvBateau2[2, 0])

        # Cas de test 4 : Variation de tous les paramètres simultanés, comparaison avec l'expression littérale
        CPx, CPy, CPz = random.choice(np.linspace(-0.05, 1)), random.choice(np.linspace(-0.01, 0.01)), random.choice(np.linspace(0,2.4))
        CP_repVoile = np.array([CPx, CPy, CPz]).reshape(-1, 1)
        O_repVoile_repBateau = np.array([random.choice(np.linspace(-0.2, 0.2)), random.choice(np.linspace(-0.2, 0.2)), random.choice(np.linspace(-0.2, 0.2))]).reshape(-1, 1)
        deltav = random.choice(np.linspace(-45,45))
        phi = random.choice(np.linspace(-50,50))
        Lambda = random.choice(np.linspace(-10,10))
        CP_repAvBateau = aero.chgt_base_pt_application(CP_repVoile, O_repVoile_repBateau, deltav, Lambda, phi)
        print("---------------------------------------------")
        print("PARAMETRES TEST CHGT BASE POINT APPLICATION :")
        print(CP_repVoile, O_repVoile_repBateau, deltav, phi, Lambda)
        #Calcul des coordonnées théoriques
        M_repBateau_repAvBateau = np.zeros((3, 3))
        cL, sL, cP, sP = np.cos(Lambda), np.sin(Lambda), np.cos(phi), np.sin(phi)
        M_repBateau_repAvBateau[0][0] = cL
        M_repBateau_repAvBateau[0][1] = -cP * sL
        M_repBateau_repAvBateau[0][2] = sP * sL
        M_repBateau_repAvBateau[1][0] = sL
        M_repBateau_repAvBateau[1][1] = cL * cP
        M_repBateau_repAvBateau[1][2] = -sP * cL
        M_repBateau_repAvBateau[2][1] = sP
        M_repBateau_repAvBateau[2][2] = cP
        cV, sV = np.cos(deltav), np.sin(deltav)
        CP_repAvBateau_th = M_repBateau_repAvBateau @ np.array([-cV*CPx+sV*CPy+O_repVoile_repBateau[0,0], -sV*CPx-cV*CPy+O_repVoile_repBateau[1,0], CPz+O_repVoile_repBateau[2,0]]).reshape(-1, 1)
        assert_array_almost_equal(CP_repAvBateau, CP_repAvBateau_th)

    def testChgt_base_forces(self):
        # Cas 1 : aucun angle de gîte, réglage de voile ou dérive.
        Vt = 10
        Vs = 2
        Lambda = 0
        angle_incidence = 0
        phi = 0
        L = 50
        D = 4
        torseur_aero_repVoile = np.concatenate((np.array([D,L,0]).reshape(-1,1),np.array([0,0,0]).reshape(-1,1)),axis=1)
        F_repAvBateau = aero.chgt_base_forces(Vt, Vs, Lambda, angle_incidence, phi, torseur_aero_repVoile)
        assert_array_almost_equal(F_repAvBateau,np.array([-D,-L,0]).reshape(-1,1))

        #Cas 2 : Caractère aléatoire de ces valeurs
        Vt = random.choice(0.51444 * np.linspace(0, 35))
        Vs = random.choice(0.51444 * np.linspace(0,4))
        Lambda = random.choice(np.linspace(-10,10))
        angle_incidence = random.choice(np.linspace(-45,45))
        phi = random.choice(np.linspace(-50,50))
        L = random.choice(0.51444 * np.linspace(5, 100))
        D = random.choice(0.51444 * np.linspace(1, 20))
        torseur_aero_repVoile = np.concatenate((np.array([D, L, 0]).reshape(-1, 1), np.array([0, 0, 0]).reshape(-1, 1)), axis=1)
        print("---------------------------------------------")
        print("PARAMETRES TEST CHGT BASE FORCES :")
        print(Vt, Vs, Lambda, angle_incidence, phi, L, D)

        F_repAvBateau = aero.chgt_base_forces(Vt, Vs, Lambda, angle_incidence, phi, torseur_aero_repVoile)

        # Calcul de la force théorique
        beta_t = -Lambda + angle_incidence  # beta_t : page 33 de [2] - angle entre axe X d'avance du bateau et vent réel"
        beta = np.pi / 2 - np.arctan((Vt * np.cos(beta_t) + Vs) / (Vt * np.sin(beta_t) * np.cos(phi)))  # beta : page 33 de [2] - angle entre axe X d'avance du bateau et vent apparent"
        Lvoile, Dvoile = np.abs(torseur_aero_repVoile[1][0]), np.abs(torseur_aero_repVoile[0][0])
        FX = Lvoile * np.sin(beta) - Dvoile * np.cos(beta)
        FY = -np.cos(phi) * (Lvoile * np.cos(beta) + Dvoile * np.sin(beta))
        FZ = -np.sin(phi) * (Lvoile * np.cos(beta) + Dvoile * np.sin(beta))
        F_repAvBateau_th = np.array([FX, FY, FZ]).reshape(-1, 1)
        assert_array_almost_equal(F_repAvBateau, F_repAvBateau_th)

if __name__=="__main__":
    unittest.main()