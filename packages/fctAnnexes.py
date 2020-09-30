def nds2ms(v):
    """
    Fonction qui convertit une vitesse exprimée en noeuds, en m/s
    --------------------
    ENTREES :
    v : une valeur de vitesse, en noeuds
    --------------------
    SORTIES :
    La vitesse v, convertie en m/s"""
    return 0.5144*v

def ms2nds(v):
    """
    Fonction qui convertit une vitesse exprimée en m/s, en noeuds
    --------------------
    ENTREES :
    v : une valeur de vitesse, en m/s
    --------------------
    SORTIES :
    La vitesse v, convertie en noeuds"""
    return v*1.944012

def interpol_lin(x, xinf, xsup, yinf, ysup):
    """Fonction qui renvoie la valeur interpolée d'une fonction en x, en interpolant linéairement entre les points inf et sup
    --------------------
    ENTREES :
    x : la valeur d'abscisse en laquelle on souhaite obtenir la valeur de la fonction
    xinf : la plus proche valeur d'abscisse inférieure à x, pour laquelle on connait la valeur de la fonction
    xsup : la plus proche valeur d'abscisse supérieure à x, pour laquelle on connait la valeur de la fonction
    yinf : la valeur de la fonction en xinf
    ysup : la valeur de la fonction en xsup
    --------------------
    SORTIES :
    La valeur de la fonction en x, interpolée linéairement entre xinf et xsup"""
    a = (ysup-yinf)/(xsup-xinf)
    return a*(x-xinf) + yinf

def trouver_lignes(workbook, alpha, Va): #Va en noeuds !!
    """Fonction qui renvoie les numéros des lignes du fichier excel associées aux valeurs inférieures et supérieures de alpha.
    NB : Fonction adaptée pour le traitement des fichiers contenant les polaires de la voile et des appendices.
    --------------------
    ENTREES :
    fichier : fichier en question duquel on souhaite extraire les données
    alpha : Angle d'incidence de la voile/appendice par rapport au fluide dans lequel il s'écoule auquel on souhaite
    connaître les valeurs de portance et traînée
            UNITE : radians
    Va : vent apparent
         UNITE : noeuds
    --------------------
    SORTIES :
    Si Va est de type "int" ou "float", il existe une feuille de calcul associée à la vitesse Va.
    La fonction renvoie alors lignes_Va, une liste sous la forme [n1, n2] où n1 et n2 sont les numéros des lignes
    correspondant aux valeurs encadrant l'angle alpha, dans la feuille de calcul Va.
    Si Va est de type "list", il n'existe pas une feuille de calcul associée à la vitesse Va et il faut interpoler entre
    deux feuilles à des vitesse différentes.
    La fonction renvoie alors un tuple (lignes_Vainf, lignes_Vasup), où lignes_Vainf et lignes_Vasup sont une liste
    de la forme [n1, n2] où n1 et n2 sont les numéros des lignes encadrant l'angle alpha dans chacune des feuilles de
    calcul Va_inf et Va_sup
    """
    if type(Va) != type([]) : # Va n'est pas une liste
        sheet = workbook[str(int(Va))+"kts"] #On ouvre la feuille de calcul correspondant au vent
        i = 4
        alpha_sup = sheet["B"+str(i+1)].value
        while alpha > alpha_sup:
            i+=1
            alpha_sup = sheet["B" + str(i+1)].value
        lignes_Va = [i, i+1]
        return lignes_Va
    else:
        Vainf = Va[0]
        Vasup = Va[1]
        #####################################
        ### Angles d'incidence pour Vainf ###
        sheet_Vainf = workbook[str(Vainf)+"kts"]
        i = 4
        alpha_sup_Vainf = sheet_Vainf["B" + str(i+1)].value
        while alpha > alpha_sup_Vainf:
            i+=1
            alpha_sup_Vainf = sheet_Vainf["B" + str(i+1)].value
        lignes_Vainf = [i, i+1]
        #####################################
        ### Angles d'incidence pour Vasup ###
        sheet_Vasup = workbook[str(Vasup)+"kts"]
        j = 4
        alpha_sup_Vasup = sheet_Vasup["B" + str(j+1)].value
        while alpha > alpha_sup_Vasup:
            j += 1
            alpha_sup_Vasup = sheet_Vasup["B" + str(j+1)].value
        lignes_Vasup = [j, j + 1]

        return lignes_Vainf, lignes_Vasup

def trouver_lignes_resistance(workbook, sheet_name, Vs_nds):
    """
    Fonction qui renvoie les numéros des lignes du fichier excel associées aux valeurs inférieures et supérieures de Vs_nds.
    NB : Fonction adaptée pour le traitement du fichier "Devis_masse.xlsx", qui contient la résistance à l'avancement.
    --------------------
    ENTREES :
    fichier : fichier en question duquel on souhaite extraire les données
    sheet_name : nom de la feuille de calcul où l'on souhaite extraire les données
    Vs_nds : vitesse du bateau
             UNITE : noeuds
    --------------------
    SORTIES :
    La fonction renvoie alors lignes, une liste sous la forme [n1, n2] où n1 et n2 sont les numéros des lignes
    correspondant aux numéros de ligne dans fichier encadrant la valeur de Vs_nds.
    """
    sheet = workbook[sheet_name]
    # Limite supprimée, remplacée par une interpolation linéaire de la résistance au dessus de 20knt afin de laisser l'algo d'optim travailler
    # if Vs_nds > 20:
    #     raise ValueError("boat speed exceding 20knots")
    i = 9
    Vs_nds_sup = sheet["AC"+str(i+1)].value
    if Vs_nds <= 20:
        while Vs_nds > Vs_nds_sup:
            i+=1
            Vs_nds_sup = sheet["AC" + str(i+1)].value
    else:
        i = 20
    lignes = [i, i+1]
    return lignes

def trouver_lignes_stab(workbook, sheet_name, angle):
    """
    Fonction qui renvoie les numéros des lignes du fichier excel associées aux valeurs inférieures et supérieures de angle.
    NB : Fonction adaptée pour le traitement du fichier "Stab_data.xlsx".
    --------------------
    ENTREES :
    fichier : fichier en question duquel on souhaite extraire les données
    sheet_name : nom de la feuille de calcul où l'on souhaite extraire les données. (soit "Trans", soit "Longi")
    angle : angle de gîte ou d'assiette, selon ce que l'on souhaite extraire.
            UNITE : degrés
    --------------------
    SORTIES :
    La fonction renvoie alors lignes, une liste sous la forme [n1, n2] où n1 et n2 sont les numéros des lignes
    correspondant aux numéros de ligne dans fichier encadrant la valeur de angle.
    """
    sheet = workbook[sheet_name]
    #print("Angle gite", angle)
    if angle < 0:
        angle_corr = -angle
    else:
        angle_corr = angle
    i = 2
    angle_sup = sheet["A"+str(i+1)].value
    while angle_corr > angle_sup:
        i+=1
        angle_sup = sheet["A" + str(i+1)].value
    lignes = [i, i+1]
    return lignes
