from math import *
import re

def Carre (x: int):
    return x * x

def Distance(x1 : int , y1 : int , x2 : int , y2 : int):
    x = sqrt(Carre(x2-x1)+(Carre(y2-y1)))
    return x

def Lecture_Fichier():
    TSP = open('bayg29.tsp', 'r')

    Name = TSP.readline().strip().split()[1]
    Type = TSP.readline().strip().split()[1]
    Comment = TSP.readline().rstrip().split()[1]   #Trouver comment extraire tout le rest ede la ligne ...
    Dimension = int(TSP.readline().strip().split()[1])
    EDGE_WEIGHT_TYPE = TSP.readline().strip().split()[1]
    linecount: int = -2
    for line in TSP:
        if 'NODE_COORD_SECTION' in line or 'DISPLAY_DATA_SECTION' in line:
            print('Appel extraction coordonnées')
            break
            # Faire appel à une fonction pour le type de Fichier qui ressemble à att48.tsp
        elif 'EDGE_WEIGHT_SECTION' in line:
            print('Appel extraction distances')
            data_extract = extractionDistances(linecount, TSP, Dimension)
            data_extract = stringToList(data_extract)
            print(data_extract)
            break
            # Faire appel à une fonction pour le type de Fichier comme bayg29.tsp
        linecount += 1
    print(Name,Type,Comment,int(Dimension),EDGE_WEIGHT_TYPE)

def extractionDistances(linecount: int, fic, dimensions: int):
    contenu = fic.readlines()
    distStr: str = ""
    for i in range(linecount, linecount + dimensions - 1):
        distStr += contenu[i]
    return distStr

def stringToList(string: str):
    str_retour = re.split('[ ]', string)
    str_retour = list(filter(None, str_retour))
    return str_retour

#def listToTab(data: list, dimensions: int):
#    for i in range(dimensions-1):
#        for j in range(dimensions - i):


Lecture_Fichier()