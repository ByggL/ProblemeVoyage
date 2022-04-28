def Lecture_Fichier():
    TSP = open('bayg29.tsp', 'r')

    Name = TSP.readline().strip().split()[1]
    Type = TSP.readline().strip().split()[1]
    Comment = TSP.readline().rstrip().split()[1]   #Trouver comment extraire tout le rest ede la ligne ...
    Dimension = int(TSP.readline().strip().split()[1])
    EDGE_WEIGHT_TYPE = TSP.readline().strip().split()[1]
    linecount: int = -2
    for line in TSP:
        if 'NODE_COORD_SECTION' in line:
            print('Appel extraction coordonnées')
            break
            # Faire appel à une fonction pour le type de Fichier qui ressemble à att48.tsp
        elif 'EDGE_WEIGHT_SECTION' in line:
            print('Appel extraction distances')
            data_extract = extractionDistances(linecount, TSP, Dimension)
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

Lecture_Fichier()