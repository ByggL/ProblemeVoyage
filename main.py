from typing import Any

from math import *
import re
import matplotlib.pyplot as plt

def Carre(x: int):
    return x * x


def Distance(x1: int, y1: int, x2: int, y2: int):
    x = sqrt(Carre(x2-x1)+(Carre(y2-y1)))
    return x


def Affichage(Tab):
    for i in range(1,30):
        if i < 10:
            print(i, end="   ")
        else:
            print(i, end="  ")
    print('(-1 pour les indexs du tableau) \n')
    print('\n'.join(['\t'.join([str(cell) for cell in row])for row in Tab]))


def MatriceAdjacente(Data: list, dimension: int):
    list_dist = []
    Y: int
    for i in range(0,dimension*2,2):
        for j in range(i+2,dimension*2,2):
            list_dist.append(round(Distance(int(Data[i]),int(Data[i+1]),int(Data[j]),int(Data[j+1]))))
        list_dist[i] = str(list_dist[i])

    print(list_dist)
    return list_dist

def extraction2(nomfic, dimensions: int, depart: int):
    # prend la matrice d'adjacence du fichier et la renvoit sous forme de string séparée
    fic = open(nomfic, 'r')
    contenu = fic.readlines()
    distStr: str = ""

    for i in range(depart, dimensions + depart):
        distStr += contenu[i]

    return distStr

def Dist_tour(data: list, Tab, dimension: int):
    Dist_total: int = 0
    for i in range(dimension-1):
        Dist_total += Tab[data[i]][data[i+1]]
    print(Dist_total)
    return Dist_total

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
            # Faire appel à une fonction pour le type de Fichier qui ressemble à att48.tsp

    chemin, liste_passage = creaChemin(Tableau, Dimension)  # création d'un chemin
    print(Name,Type,Comment,int(Dimension),EDGE_WEIGHT_TYPE)
    affchemin(chemin, Dimension)  # affichage du chemin trouvé
    Dist_tour(liste_passage,Tableau,Dimension)

    xo = [x[o] for o in liste_passage + [liste_passage[0]]]
    yo = [y[o] for o in liste_passage + [liste_passage[0]]]

    plt.plot(xo, yo, "o")

    plt.show()
    TSP.close()


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
    Affichage(Tab)
    return Tab

def plusCourtDist(Tab, numVille, dimensions,passedlist):
    # trouve la ville la plus proche d'une ville donnée et renvoie son index sur le tableau
    # en parcourant la ligne du tableau correspondant à la ville donnée
    plusPetit: int = 1000
    indexPlusPetit = 0

    for j in range(dimensions):
        if Tab[numVille][j] < plusPetit and Tab[numVille][j] != 0 and j+1 not in passedlist:  # vérifie si la distance est la plus petite parmi celles
            plusPetit = Tab[numVille][j]                                                      # vérifiées, si elle n'est pas égale à 0 et si la ville
            indexPlusPetit = j                                                                # correspondant à la distance n'est pas déjà passée

    coordretour: list = [numVille, indexPlusPetit]  # faire en sorte que le code se reproduise pour la ligne i+2
    return coordretour


def creaChemin(Tab, dimensions):
     # crée une liste des numéros de villes selon le chemin le plus court passant une seule fois par chaque ville
    suiteCoord = []  # liste à retourner
    passedlist = [1]  # liste de vérification des villes déjà passées
    pluscourt = plusCourtDist(Tab,0,dimensions, passedlist)     #
    suiteCoord.append(pluscourt)                                # initialisation du chemin
    passedlist.append(pluscourt[1] + 1)                         #

    for g in range(dimensions - 1):
        pluscourtloop = plusCourtDist(Tab, suiteCoord[g][1], dimensions, passedlist)
        suiteCoord.append(pluscourtloop)
        passedlist.append(pluscourtloop[1] + 1)

    print(passedlist)
    return suiteCoord, passedlist


def affchemin(chemin, dimensions):
    print("-1 pour les indices")

    for i in range(dimensions):
        print(chemin[i][0] + 1, " --> ", chemin[i][1] + 1)

Lecture_Fichier()