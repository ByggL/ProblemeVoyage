def Lecture_Fichier():
    TSP = open('bayg29.tsp', 'r')

    Name = TSP.readline().strip().split()[1]
    Type = TSP.readline().strip().split()[1]
    Comment = TSP.readline().rstrip().split()[1]   #Trouver comment extraire tout le rest ede la ligne ...
    Dimension = TSP.readline().strip().split()[1]
    EDGE_WEIGHT_TYPE = TSP.readline().strip().split()[1]
    for line in TSP:
        if 'NODE_COORD_SECTION' in line:
            print('Appel extraction coordonnées')
            break
            # Faire appel à une fonction pour le type de Fichier qui ressemble à att48.tsp
        elif 'EDGE_WEIGHT_SECTION' in line:
            print('Appel extraction distances')
            break
            # Faire appel à une fonction pour le type de Fichier comme bayg29.tsp
    print(Name,Type,Comment,int(Dimension),EDGE_WEIGHT_TYPE)

Lecture_Fichier()