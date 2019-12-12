def demande_mot() -> str:
    lettre_unique: bool = False

    # demainde un mot de 7 lettres au joueur 1

    while lettre_unique == False:
        lettre_unique = True
        mot: str = input("Entrez un mot de 7 lettres uniques : ")

        for car in mot:
            if mot.count(car) > 1:
                lettre_unique = False

    return mot


def resultat_jeu(_mot_a_trouver: str, _proposition: str) -> str:
    resultat: str = ""

    for i in range(len(_mot_a_trouver)):  # on cherche l'index pour cela quon fait un range
        if _proposition[i] == _mot_a_trouver[i]:
            resultat += _proposition[i]

        elif _proposition[i] in _mot_a_trouver:  ## on regarde si la lettre est dans le mot ( dans le cas ou il est pas au meme index)
            # version avec find --> elif _mot_a_trouver.find(_proposition[i]) != -1:
            resultat += _proposition[i].lower()  ## on met lower ici car on a tout mis en maj précédement
        else:
            resultat += "."

    return resultat

def moyenne_tentatives(_liste: list) -> float:
    total_tentative: int = 0

    for nb_tent in _liste:
        total_tentative += nb_tent

    return round(total_tentative / len(_liste), 1) ## virgule 1 car on arrondi à 1 chiffre apres la virgg




### Programme principal
saisie_j1: str
saisie_j2: str
resultat: str = ""
choix: str = 'o'
nb_tentative: int = 0
liste_tentatives: list = []

while choix == 'o':
    print("JOUEUR 1")
    saisie_j1 = demande_mot().upper()  ## afin de comparer la meme pour j1 et j2 ( on a mis upper a j2 aussi )

    print("\nJOUEUR 2 \nLe mot à trouver commence par un", saisie_j1[0])
    saisie_j2 = demande_mot().upper()
    resultat = resultat_jeu(saisie_j1, saisie_j2)
    nb_tentative = 1

    # Tant que le mot proposé est différent du mot à trouvé le joueur 2 joue
    while saisie_j1 != resultat:
        print(resultat)
        saisie_j2 = demande_mot().upper()
        resultat = resultat_jeu(saisie_j1, saisie_j2)
        nb_tentative += 1

    liste_tentatives.append(nb_tentative)
    print("Bravo vous avez trouvé, le mot était", resultat)

    choix = input("Voulez vous rejouer ? oui[o], non[n]")

print("Nombre moyen de tentatives:", moyenne_tentatives(liste_tentatives))
