import random
from Case import Case
from Motif import Motif
from Grille import Grille

def creer_grille_jeu(grille, difficulte="moyen"):
    """
    Retire des chiffres en laissant plus d'indices selon la difficulté choisie.
    difficulte peut être 'facile', 'moyen' ou 'difficile'.
    """
    cases = [grille.cases[l][c] for l in range(grille.lignes) for c in range(grille.colonnes)]
    random.shuffle(cases)

    # On définit combien de cases maximum on s'autorise à vider
    # Sur une grille 8x8 (64 cases) :
    if difficulte == "facile":
        max_cases_a_vider = int(len(cases) * 0.4)   # ~25 cases vides (39 indices)
    elif difficulte == "moyen":
        max_cases_a_vider = int(len(cases) * 0.6)   # ~38 cases vides (26 indices)
    else: # difficile
        max_cases_a_vider = int(len(cases) * 0.85)  # un maximum de cases vides

    cases_videes = 0

    for case in cases:
        if cases_videes >= max_cases_a_vider:
            # On a assez enlevé de chiffres, on verrouille le reste des chiffres pour le joueur
            if case.valeur is not None:
                case.fixe = True
            continue

        valeur_origine = case.valeur
        case.valeur = None

        # On vérifie si la solution reste unique
        if grille.resoudre_complet() == 1:
            cases_videes += 1
        else:
            # Si retirer ce chiffre crée une ambiguïté, on le remet et il devient un indice fixe
            case.valeur = valeur_origine
            case.fixe = True