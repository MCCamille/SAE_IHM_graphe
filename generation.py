import random
from Case import Case
from Motif import Motif
from Grille import Grille

def creer_grille_jeu(grille):
    """Retire un maximum de chiffres tout en garantissant l'unicité de la solution."""
    # On liste toutes les cases de la grille et on les mélange
    cases = [grille.cases[l][c] for l in range(grille.lignes) for c in range(grille.colonnes)]
    random.shuffle(cases)

    for case in cases:
        # On sauvegarde la valeur d'origine au cas où
        valeur_origine = case.valeur
        
        # On retire le chiffre
        case.valeur = None

        # On demande au solveur combien il trouve de solutions
        # (S'il en trouve 1, c'est parfait, le jeu reste résolvable de manière unique)
        if grille.resoudre_complet() != 1:
            # S'il en trouve 0 ou 2+, on remet la valeur d'origine !
            case.valeur = valeur_origine
            case.fixe = True # Cette case fera partie des indices de départ du joueur