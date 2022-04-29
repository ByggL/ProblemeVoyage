from math import *
import re

def Carre (x: int):
    return x * x

def Distance(x1 : int , y1 : int , x2 : int , y2 : int):
    x = sqrt(Carre(x2-x1)+(Carre(y2-y1)))
    return x

def Affichage(Tab):
    print('\n'.join(['\t'.join([str(cell) for cell in row])for row in Tab]))

def MatriceAdjacente(Data: list , dimension: int):
    X: int = 0
    Y: int = 0
    Tab = [[0 for i in range(dimensions - 1)] for j in range(dimensions - 1)]

    for i in range(1,dimension-1):
        for j in range(i,dimension-1):
            Tab[i][j] = Distance(Data[i+X],Data[i+1+X],Data[j+Y],Data[j+1+Y])
            Y += 3
        X += 3



def Lecture_Fichier():
    TSP = open('bayg29.tsp', 'r')

    Name = TSP.readline().strip().split()[1]
    Type = TSP.readline().strip().split()[1]
    Comment = TSP.readline().rstrip().split()[1]   #Trouver comment extraire tout le reste de la ligne ...
    Dimension = int(TSP.readline().strip().split()[1])
    EDGE_WEIGHT_TYPE = TSP.readline().strip().split()[1]
    linecount: int = -2
    for line in TSP:
        if 'NODE_COORD_SECTION' in line or 'DISPLAY_DATA_SECTION' in line:
            print('Appel extraction coordonnées')
            coord_extract = extraction(linecount, TSP, Dimension)
            print(coord_extract)
            stringToList(coord_extract)
            MatriceAdjacente(coord_extract, Dimension)
            break
            # Faire appel à une fonction pour le type de Fichier qui ressemble à att48.tsp
        elif 'EDGE_WEIGHT_SECTION' in line:
            print('Appel extraction distances')
            data_extract = extraction(linecount, TSP, Dimension)
            data_extract = stringToList(data_extract)
            print(data_extract)
            Tableau = listToTab(data_extract, Dimension)
            break
            # Faire appel à une fonction pour le type de Fichier comme bayg29.tsp
        linecount += 1
    chemin = creaChemin(Tableau, Dimension)
    print(Name,Type,Comment,int(Dimension),EDGE_WEIGHT_TYPE)
    print(chemin)

def extraction(linecount: int, fic, dimensions: int):
    contenu = fic.readlines()
    distStr: str = ""
    for i in range(linecount, linecount + dimensions - 1):
        distStr += contenu[i]
    return distStr

def stringToList(string: str):
    str_retour = re.split('[ \n  ]', string)
    str_retour = list(filter(None, str_retour))
    return str_retour

def listToTab(data: list, dimensions: int):
    X: int = 0
    Tab = [[0 for i in range(dimensions-1)] for j in range(dimensions-1)]

    for i in range(dimensions-1):
        for j in range(i, dimensions - 1):
            Tab[i][j] = int(data[X])
            X += 1
    Affichage(Tab)
    return Tab

def plusCourtLigne(Tab, ligne, dimensions):
    plusPetit: int = Tab[ligne][0]
    for i in range(1, dimensions-1):
        if Tab[ligne][i] < plusPetit and Tab[ligne][i] != 0:
            plusPetit = Tab[ligne][i]
    coordretour: list = [ligne+1, i+2] #faire en sorte que le code se reproduise pour la ligne i+2
    return coordretour

def creaChemin(Tab, dimensions):
    suiteCoord = []
    suiteCoord.append(plusCourtLigne(Tab, 0, dimensions))
    for g in range(1, dimensions - 1):
        suiteCoord.append(plusCourtLigne(Tab, suiteCoord[g - 1][1] - 2, dimensions))
    return suiteCoord


Lecture_Fichier()