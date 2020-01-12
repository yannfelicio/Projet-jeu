from outils import est_egal_a, coordonnee_x, coordonnee_y, creer_caisse, creer_case_vide, creer_cible, creer_image, \
    creer_mur, creer_personnage
import time
import os


# Fonctions à développer

def jeu_en_cours(caisses,
                 cibles) -> bool:  # quel est la condition de la fin du jeu, si toute les caisse sont sur les cible c'est fini
    ''' #les boxes ont une coordonné x et y
    Fonction testant si le jeu est encore en cours et retournant un booléen comme réponse sur l'état de la partie.
    :param caisses: La liste des caisses du niveau en cours
    :param cibles: La liste des cibles du niveau en cours
    :return: True si la partie est finie, False sinon
    '''
    arret: bool = False
    cpt: int = 0
    # regarder si une caisse est sur cible, #comparer les deux listes
    # for i in caisses:

    for i in cibles:
        for j in caisses:
            if est_egal_a(j, i):
                cpt += 1
    if cpt == len(cibles):
        arret = True
    return arret

def charger_niveau(joueur, caisses, cibles, murs, path):
    '''
    Fonction permettant de charger depuis un fichier.txt et de remplir les différentes listes permettant le
    fonctionnement du jeu (joueur, caisses, murs, cibles)
    :param joueur: liste des personnages
    :param caisses: liste des caisses
    :param cibles: liste des cibles
    :param murs: liste des murs
    :param path: Chemin du fichier.txt
    :return:
    '''
    cpt_x: int = 0
    cpt_y: int = 0
    with open(path, "r") as filin:
        lignes: list = filin.readlines()

        for i in lignes:

            for j in i:

                if j == "#":
                    # faire deux boucles imbriqués, 20, 20 est la position initiale un for pour x et un for pour y
                    # 32 étant l'espace entre deu éléments.  20 + 0 * 32 /// 20 étant l'espace entre le fichier texte et le premier bloc
                    # du coup 20 et 32 reste il n'y a juste le 0 qui va varier

                    murs.append(creer_mur(X_PREMIERE_CASE + (DISTANCE_ENTRE_CASE * cpt_x),
                                          Y_PREMIERE_CASE + (DISTANCE_ENTRE_CASE * cpt_y)))

                elif j == ".":
                    cibles.append(creer_cible(X_PREMIERE_CASE + (DISTANCE_ENTRE_CASE * cpt_x),
                                              Y_PREMIERE_CASE + (DISTANCE_ENTRE_CASE * cpt_y)))
                elif j == "$":
                    caisses.append(creer_caisse(X_PREMIERE_CASE + (DISTANCE_ENTRE_CASE * cpt_x),
                                                Y_PREMIERE_CASE + (DISTANCE_ENTRE_CASE * cpt_y)))
                elif j == "@":
                    joueur.append(creer_personnage(X_PREMIERE_CASE + (DISTANCE_ENTRE_CASE * cpt_x),
                                                   Y_PREMIERE_CASE + (DISTANCE_ENTRE_CASE * cpt_y)))
                cpt_x += 1
            cpt_y += 1
            cpt_x = 0


def mouvement(direction, can, joueur, murs, caisses, liste_image):
    '''
    Fonction permettant de définir les cases de destinations (il y en a 2 si le joueur pousse une caisse) selon la
    direction choisie.
    :param direction: Direction dans laquelle le joueur se déplace (droite, gauche, haut, bas)
    :param can: Canvas (ignorez son fonctionnement), utile uniquement pour créer_image()
    :param joueur: liste des joueurs
    :param murs: liste des murs
    :param caisses: liste des caisses
    :param liste_image: liste des images (murs, caisses etc...) détaillée dans l'énoncé
    :return:
    '''
    
    # il n'y a qu'une seule liste à la fois qui bouge, soit x, soit y, a gauche et droite c'est y et haut bas = x
    # Lorsqu'on fait un mouvement, on crée une case vide aux coordonnées de la destination
    if direction == "gauche":
        coordonnee_destination = creer_case_vide(coordonnee_x(joueur[0]) - DISTANCE_ENTRE_CASE, coordonnee_y(joueur[0]))
        coordonnee_case_suivante = creer_case_vide(coordonnee_x(joueur[0]) - (DISTANCE_ENTRE_CASE * 2),
                                                   coordonnee_y(joueur[0]))

    if direction == "droite":
        coordonnee_destination = creer_case_vide(coordonnee_x(joueur[0]) + DISTANCE_ENTRE_CASE, coordonnee_y(joueur[0]))
        coordonnee_case_suivante = creer_case_vide(coordonnee_x(joueur[0]) + (DISTANCE_ENTRE_CASE * 2),
                                                   coordonnee_y(joueur[0]))

    if direction == "haut":
        coordonnee_destination = creer_case_vide(coordonnee_x(joueur[0]), coordonnee_y(joueur[0]) - DISTANCE_ENTRE_CASE)
        coordonnee_case_suivante = creer_case_vide(coordonnee_x(joueur[0]),
                                                   coordonnee_y(joueur[0]) - (DISTANCE_ENTRE_CASE * 2))

    if direction == "bas":
        coordonnee_destination = creer_case_vide(coordonnee_x(joueur[0]), coordonnee_y(joueur[0]) + DISTANCE_ENTRE_CASE)
        coordonnee_case_suivante = creer_case_vide(coordonnee_x(joueur[0]),
                                                   coordonnee_y(joueur[0]) + (DISTANCE_ENTRE_CASE * 2))
    
    # on crée la variable ancienne_caisse que l'on va utiliser dans la fonction effectuer_mouvement
    # cela va permettre de conserver les coordonées afin de pouvoir supprimer l'ancienne caisse
    ancienne_caisse = coordonnee_destination
    # on crée les variables deplace pour les utilisé dans la fonction effectuer_mouvement
    deplace_joueur_x = coordonnee_x(coordonnee_destination)
    deplace_joueur_y = coordonnee_y(coordonnee_destination)
    deplace_caisse_x = coordonnee_x(coordonnee_case_suivante)
    deplace_caisse_y = coordonnee_y(coordonnee_case_suivante)
    
    # on appele la fonction effectuer_mouvement ici car elle est appelée par mouvement ( selon la direction ) 
    effectuer_mouvement(coordonnee_destination, coordonnee_case_suivante, ancienne_caisse, caisses, murs, joueur, can,
                        deplace_caisse_x, deplace_caisse_y, deplace_joueur_x, deplace_joueur_y, liste_image)


def effectuer_mouvement(coordonnee_destination, coordonnee_case_suivante, ancienne_caisse, caisses, murs, joueur, can,
                        deplace_caisse_x, deplace_caisse_y, deplace_joueur_x, deplace_joueur_y, liste_image):
    '''
    Fonction permettant d'effectuer le déplacement ou de ne pas l'effectuer si celui-ci n'est pas possible. Voir énoncé
    "Quelques règles". Cette methode est appelée par mouvement.
    :param coordonnee_destination: variable CaseVide ayant possiblement des coordonnées identiques à une autre variable
    (murs, caisse, casevide)
    :param coordonnee_case_suivante: variable CaseVide ayant possiblement des coordonnées identiques à une autre variable
    (murs, caisse, casevide) mais représente la case après coordonnee_destination
    :param ancienne_caisse: variable utile pour supprimer l'ancienne caisse (après avoir déplacé celle-ci)
    :param caisses: liste des caisses
    :param murs: liste des murs
    :param joueur: liste des joueurs
    :param can: Canvas (ignorez son fonctionnement), utile uniquement pour créer_image()
    :param deplace_caisse_x: coordonnée à laquelle la caisse va être déplacée en x (si le joueur pousse une caisse)
    :param deplace_caisse_y: coordonnée à laquelle la caisse va être déplacée en y (si le joueur pousse une caisse)
    :param deplace_joueur_x: coordonnée en x à laquelle le joueur va être après le mouvement
    :param deplace_joueur_y: coordonnée en y à laquelle le joueur va être après le mouvement
    :param liste_image: liste des images (murs, caisses etc...) détaillée dans l'énoncé
    :return:
    '''

    if coordonnee_destination in murs:  # si un mur alors je bouge pas
        pass

    elif coordonnee_destination in caisses:
        if coordonnee_case_suivante in caisses or coordonnee_case_suivante in murs:  # si double caisse alors je bouge pas
            pass
        else:
            for c in caisses:
                if est_egal_a(c, ancienne_caisse):
                    caisses.remove(c)
                    joueur.append(creer_personnage(deplace_joueur_x, deplace_joueur_y))
                    ancien_joueur = joueur.pop(0)
                    creer_image(can, coordonnee_x(ancien_joueur), coordonnee_y(ancien_joueur), liste_image[6])
                    caisses.append(creer_caisse(deplace_caisse_x, deplace_caisse_y))

    else:
        joueur.append(creer_personnage(deplace_joueur_x, deplace_joueur_y))
        ancien_joueur = joueur.pop(0)
        creer_image(can, coordonnee_x(ancien_joueur), coordonnee_y(ancien_joueur), liste_image[6])

def chargement_score(scores_file_path, dict_scores):
    '''
    Fonction chargeant les scores depuis un fichier.txt et les stockent dans un dictionnaire
    :param scores_file_path: le chemin d'accès du fichier
    :param dict_scores:  le dictionnaire pour le stockage
    :return:
    '''
    liste_score: list = []

    with open(scores_file_path, "r") as fichier:
        for lignes in fichier:
            lignes = lignes.strip() # fonction .strip() afin d'enlever les \n en fin de ligne
            lignes = lignes[:-1] # on supprime le dernier caractère -> ;
            lignes = lignes.split(";") # on découpe les bloc de caractère séparer par un ; en liste 

            for i in range(1, len(lignes)):
                liste_score.append(int(lignes[i])) # on insert le contenu de la liste en int afin de pouvoir trier par ordre décroissant

            dict_scores[lignes[0]] = sorted(liste_score, reverse=True)# fonction qui permet de trier la liste des score du plus grand au plus petit
            liste_score = [] # on remet la liste score à zero pour la prochaine ligne

def maj_score(niveau_en_cours, dict_scores) -> str:
    '''
    Fonction mettant à jour l'affichage des scores en stockant dans un str l'affichage visible
    sur la droite du jeu.
    ("Niveau x
      1) 7699
      2) ... ").
    :param niveau_en_cours: le numéro du niveau en cours
    :param dict_scores: le dictionnaire pour stockant les scores
    :return str: Le str contenant l'affichage pour les scores ("\n" pour passer à la ligne)
    '''

    scores: str = ""
    new_scores: str = "Niveau " + niveau_en_cours + "\n"
        
    for i in range(len(dict_scores[niveau_en_cours])):
        scores = str(i + 1) + " )" + " " + str(dict_scores[niveau_en_cours][i]) + "\n"
        new_scores += scores
    
    return new_scores


def enregistre_score(temps_initial, nb_coups, score_base, dict_scores, niveau_en_cours) -> int:
    '''
    Fonction enregistrant un nouveau score réalisé par le joueur. Le calcul de score est le suivant :
    score_base - (temps actuel - temps initial) - (nombre de coups * valeur d'un coup)
    Ce score est arrondi sans virgule et stocké en tant que int.
    :param temps_initial: le temps initial
    :param nb_coups: le nombre de coups que l'utilisateurs à fait (les mouvements)
    :param score_base: Le score de base identique pour chaque partie
    :param dict_scores: Le dictionnaire stockant les scores
    :param niveau_en_cours: Le numéro du niveau en cours
    :return: le score sous forme d'un int
    '''
    temps_actuel = time.time()# time.time() nous donne le temps au moment de l'appel
    nouveau_score: int = 0
    nouveau_score = round(score_base - (temps_actuel - temps_initial) - (nb_coups * VALEUR_COUP))

    for i in range(len(dict_scores[niveau_en_cours])):

        if int(dict_scores[niveau_en_cours][i]) < nouveau_score:

            dict_scores[niveau_en_cours].insert(i, str(nouveau_score))
            dict_scores[niveau_en_cours].pop(i)
            break
    # niveau_en_cours est un str, on insert le nouveau score dans le dico selon le niveau
    return nouveau_score

def update_score_file(scores_file_path, dict_scores):
    '''
    Fonction sauvegardant tous les scores dans le fichier.txt.
    :param scores_file_path: le chemin d'accès du fichier de stockage des scores
    :param dict_scores: Le dictionnaire stockant les scores
    :return:
    '''
    texte_score: str = ""

    for key, value in dict_scores.items(): # .imets nous permet de récuperer chaque clé et ses valeurs
        texte_score += str(key) + ";"
        for score in value:
            texte_score += str(score) + ";"
        texte_score += "\n"


    with open(scores_file_path, "w") as fillin:

        fillin.write(texte_score)
        fillin.close()

# Constantes à utiliser

DISTANCE_ENTRE_CASE = 32  # distance par rapport à l'autre case
VALEUR_COUP = 50
X_PREMIERE_CASE = 20
Y_PREMIERE_CASE = 20

# Ne pas modifier !
if __name__ == '__main__':
    os.system("fourni\simulateur.py")
