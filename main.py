from math import *
import re
import matplotlib.pyplot as plt


def extraction2(nomfic, dimensions: int, depart: int):
    # prend la matrice d'adjacence du fichier et la renvoit sous forme de string séparée
    fic = open(nomfic, 'r')
    contenu = fic.readlines()
    distStr: str = ""

    for i in range(depart, dimensions + depart):
        distStr += contenu[i]

    return distStr


def Lecture_Fichier():
    nomfic = 'bayg29.tsp'
    TSP = open(nomfic, 'r')  # ouverture du fichier
    Name = TSP.readline().strip().split()[1]
    Type = TSP.readline().strip().split()[1]
    Comment = TSP.readline().strip().split()[1]   #Trouver comment extraire tout le reste de la ligne ...
    Dimension = TSP.readline()
    Dimension = Dimension.replace(' :',':')
    Dimension = int(Dimension.strip().split()[1])
    EDGE_WEIGHT_TYPE = TSP.readline().strip().split()[1]

    for line in TSP:  # parcours du fichier
        if line.strip('\n') == 'EDGE_WEIGHT_SECTION':  # si matrice d'adjacence trouvée d'abord
            print('Appel extraction distances')
            data_extract = stringToList(extraction2(nomfic, Dimension, 8))  # extraction de la matrice sous forme de string puis en liste
            Tableau = listToTab(data_extract, Dimension)  # transformation de la matrice en tableau pour traitement
            # Faire appel à une fonction pour le type de Fichier comme bayg29.tsp

            coord_extract = stringToList(extraction2(nomfic, Dimension, 8+Dimension))
            for i in range(Dimension):
                coord_extract[i*3] = ""
            coord_extract = list(filter(None, coord_extract))

            x = [float(coord_extract[i]) for i in range(0, len(coord_extract), 2)]
            y = [float(coord_extract[i]) for i in range(1, len(coord_extract), 2)]

            print(x, '\n', y)

        if line.strip('\n') == 'NODE_COORD_SECTION' or line == 'DISPLAY_DATA_SECTION':  # si des coordonnées trouvées d'abord
            print('Appel extraction coordonnées')
            coord_extract = extraction2(nomfic, Dimension, 6)
            print(coord_extract)
            coord_extract = stringToList(coord_extract)
            for i in range(0,Dimension*2,2):
                del coord_extract[i]
            Data = MatriceAdjacente(coord_extract, Dimension)
            Tableau = listToTab(Data, Dimension)

            x = [float(coord_extract[i]) for i in range(0, len(coord_extract), 2)]
            y = [float(coord_extract[i]) for i in range(1, len(coord_extract), 2)]
            # Faire appel à une fonction pour le type de Fichier qui ressemble à att48.tsp

    liste_passage = creaChemin(x, y, Dimension)  # création d'un chemin
    print(Name,Type,Comment,int(Dimension),EDGE_WEIGHT_TYPE)
    affchemin(liste_passage, Dimension)  # affichage du chemin trouvé
    print(longueurTour(x, y, liste_passage))
    test_objectif: list = [1, 28, 6, 12, 9, 26, 3, 29, 5, 21, 2, 20, 10, 4, 15, 18, 14, 17, 22, 11, 19, 25, 7, 23, 8, 27, 16, 13, 24, 1]
    print(longueurTour(x, y, test_objectif))

    xo = [x[o-1] for o in liste_passage]
    yo = [y[o-1] for o in liste_passage]

    plt.plot(xo, yo, "o-")

    plt.show()
    TSP.close()


############################################### création matrice d'adjacence sous forme de tableau #####################
def stringToList(string: str):
    str_retour = re.split('[ \n  ]', string)
    str_retour = list(filter(None, str_retour))
    return str_retour


def listToTab(data: list, dimensions: int):
    # transforme une liste en tableau d'adjacence (avec dimensions de la matrice)
    X: int = 0
    Tab = [[0 for i in range(dimensions)] for j in range(dimensions)]
    for i in range(1,dimensions):
        for j in range(i, dimensions):
            Tab[i-1][j] = int(data[X])
            Tab[j][i-1] = int(data[X])
            X += 1
    return Tab


def Distance(x1: int, y1: int, x2: int, y2: int):
    x = sqrt((x2-x1)**2+((y2-y1)**2))
    return x


def MatriceAdjacente(Data: list, dimension: int):  # pour créer une matrice seulement à partir de coordonnées
    list_dist = []
    Y: int
    for i in range(0,dimension*2,2):
        for j in range(i+2,dimension*2,2):
            list_dist.append(round(Distance(int(Data[i]),int(Data[i+1]),int(Data[j]),int(Data[j+1]))))
        list_dist[i] = str(list_dist[i])

    print(list_dist)
    return list_dist
########################################################################################################################


############################################### création du chemin le plus court entre les villes ######################
def creaChemin(x, y, dimensions):
    # crée une liste des numéros de villes selon le chemin le plus court passant une seule fois par chaque ville
    passedlist: list = []

    for i in range(1,dimensions+1):
        passedlist.append(i)

    passedlist.append(1)

    passedlist = permutation(x, y, passedlist, len(passedlist))

    print(passedlist)
    return passedlist


def longueurTour(x,y, ordre):  # x et y les listes de coordonnées, ordre la liste des passages
    i = ordre[-1]
    x0, y0 = x[i], y[i]
    d = 0
    for o in ordre:
        x1, y1 = x[o-1], y[o-1]
        d += (x0-x1)**2 + (y0-y1)**2
        x0, y0 = x1, y1
    return d


def permutation(x, y, liste_pass: list, dimensions):
    longueur = longueurTour(x, y, liste_pass)  # assigne la longueur de l'ordre initial à d
    longueur0 = longueur+1
    it: int = 1  # comptage des itérations
    while longueur < longueur0:
        it += 1
        print("itération", it, " : distance =", longueur)
        longueur0 = longueur
        for i in range(1, dimensions-1):
            for j in range(i+2, dimensions):
                segment: list = liste_pass[i:j].copy()  # copie dans 'segment' le segment de l'ordre entre les indices i et j
                segment.reverse()  # inverse la liste 'segment'
                liste_pass2 = liste_pass[:i] + segment + liste_pass[j:]  # reconstitue l'ordre en y mettant le segment inversé
                nouv_longueur = longueurTour(x, y, liste_pass2)  # calcule la longueur de ce nouvel ordre

                if nouv_longueur < longueur:  # si la longueur du nouvel ordre est plus petite que l'ordre original
                    longueur = nouv_longueur  # la longueur du nouvel ordre remplace la longueur originale
                    liste_pass = liste_pass2  # le nouvel ordre remplace l'ordre original
    return liste_pass
########################################################################################################################


############################################### fonctions d'affichage ##################################################
def affchemin(chemin, dimensions):
    print("-1 pour les indices")

    for i in range(dimensions-1):
        print(chemin[i], " --> ", chemin[i+1])


def Affichage(Tab):
    for i in range(1,30):
        if i < 10:
            print(i, end="   ")
        else:
            print(i, end="  ")
    print('(-1 pour les indexs du tableau) \n')
    print('\n'.join(['\t'.join([str(cell) for cell in row])for row in Tab]))


Lecture_Fichier()