import tsplib95

fic = open("aayg29.tsp", "r")
fullStr: str = fic.read()
lines = fic.readlines()
print(fullStr)
for line in fic:
    print(lines[line])