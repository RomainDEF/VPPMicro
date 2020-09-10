import numpy as np
from openpyxl import load_workbook
from packages import aero, fctAnnexes
import matplotlib.pyplot as plt
# l'idée là est d'importer toutes les données nécessaires et ne variants pas.
#
rho_air = 1.225
rho_eau = 1025
DELTA = 72
theta = 0.017453293

workbookAero = load_workbook(filename="data/Polaires_Voile_data4.xlsm", data_only=True)

def Tracé_en_allure():
    PHI = np.deg2rad(0)
    Vt = fctAnnexes.nds2ms(15)
    Vs = fctAnnexes.nds2ms(5)
    LAMBDA = np.deg2rad(0)
    L_angle_allure_deg = np.linspace(10,170)
    L_angle_allure = np.deg2rad(L_angle_allure_deg)
    L_Fxtot = []
    L_Fxaero = []
    L_Fxsafran = []
    L_Fxquille = []
    L_Fxstab = []
    L_Fxresistance = []
    for angle in L_angle_allure:
        T_aero = aero.torseur_Faero(Vt, Vs, angle, LAMBDA, PHI, rho_eau, rho_air, workbookAero)
        Fx_aero = T_aero[0][0]
        L_Fxaero.append(Fx_aero)


    # plt.plot(L_angle_allure_deg, L_Fxtot, label = "Fx_total")
    plt.plot(L_angle_allure_deg, L_Fxaero, label = "Fx_aero")
    # plt.plot(L_angle_allure_deg, L_Fxquille, label = "Fx_quille")
    # plt.plot(L_angle_allure_deg, L_Fxsafran, label = "Fx_safran")
    # plt.plot(L_angle_allure_deg, L_Fxstab, label = "Fx_stab")
    # plt.plot(L_angle_allure_deg, L_Fxresistance, label = "Fx_resistance")
    plt.ylabel("Fx (N)")
    plt.xlabel("TWA (deg)")
    plt.legend()
    plt.show()


if __name__=="__main__":
    Tracé_en_allure()
    plt.show()
