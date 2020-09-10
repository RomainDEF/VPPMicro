import os


def writeFile_bilan(filename, path, Vt, data_list):
    """data_list => Liste de listes contenant les valeurs à écrire dans le fichier texte :"""
    os.chdir(path)
    with open(filename+'.txt','w') as f:
        f.write("____________________________________________________\n")
        f.write("PARAMETRES DE SIMULATION \n")
        f.write("Vent réel Vt (kt)                  "+str(Vt)+"\n")
        f.write ("_________________________________________________________________________________________\n")
        f.write ("Angle allure (m/s)|     Vs (m/s)     |     Phi (rad)    |   Lambda (rad)   |      Fx (N)      |      Fy (N)      |     Mx (N.m)     \n")
        f.write ("-----------------------------------------------------------------------------------------\n")
        n = len(data_list[0])
        m = len(data_list)
        for i in range (n): # On parcourt les résultats itération par itération
            st = "  "
            l_value = 12 #Longueur d'une donnée
            for j in range(m): #On parcourt pour l'itération i, les valeurs de chaque grandeur qu'on souhaite encoder
                st2add = str("%.3e"%data_list[j][i])
                if len(st2add)<l_value:
                    st2add = (l_value-len(st2add))*" "+st2add
                else: #la valeur est trop grande est arrondit
                    st2add = st2add[:l_value]
                st = st + st2add + " "*7
            f.write(st+"\n")
    os.chdir('../..')

def writeFile_rawdata(filename, path, Vt, angle, data_list):
    """data_list => Liste de listes contenant les valeurs à écrire dans le fichier texte :"""
    os.chdir(path)
    with open(filename+'.txt','w') as f:
        f.write("____________________________________________________\n")
        f.write("PARAMETRES DE SIMULATION \n")
        f.write("Vent réel Vt (kt)                  "+str(Vt)+"\n")
        f.write("Angle d'allure (deg)               "+str(angle)+"\n")
        f.write ("_____________________________________________________________________________________________________\n")
        f.write ("    Vs (m/s)    |    phi (rad)   |  Lambda (rad)  |     Fx (N)     |     Fy (N)     |    Mx (N.m)    \n")
        n = len(data_list[0])
        m = len(data_list)
        for i in range (n): # On parcourt les résultats itération par itération
            st = "  "
            l_value = 12 #Longueur d'une donnée
            for j in range(m): #On parcourt pour l'itération i, les valeurs de chaque grandeur qu'on souhaite encoder
                st2add = str("%.3e"%data_list[j][i])
                if len(st2add)<l_value:
                    st2add = (l_value-len(st2add))*" "+st2add
                else: #la valeur est trop grande est arrondit
                    st2add = st2add[:l_value]
                st = st + st2add + "  |  "
            f.write(st+"\n")
    os.chdir('../../..')