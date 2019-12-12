with open("niveaux/level1.txt", "r") as filin:
    lignes: list = filin.readlines()
    for i in lignes:
        print(i)
