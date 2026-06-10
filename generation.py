from Grille import Grille
from Motif import Motif
from Case import Case
import random


def prochaine_case_vide(grille):
    for l in range(grille.nb_lignes):
        for c in range(grille.nb_colonnes):
            if grille.cases[l][c].est_vide():
                return grille.cases[l][c]
    return None


def valeurs_possibles(grille, case):
    motif = grille.motifs[case.id_motif]

    deja_dans_motif = set(motif.valeurs_presentes())
    deja_chez_voisins = {
        voisin.valeur
        for voisin in grille.obtenir_voisins(case)
        if voisin.valeur is not None
    }

    possibles = [
        v for v in range(1, motif.taille + 1)
        if v not in deja_dans_motif and v not in deja_chez_voisins
    ]

    random.shuffle(possibles)
    return possibles


def resoudre(grille):
    case = prochaine_case_vide(grille)

    if case is None:
        return True

    for valeur in valeurs_possibles(grille, case):
        case.valeur = valeur

        if resoudre(grille):
            return True

        case.valeur = None

    return False


# ============================================================
# GÉNÉRATION DES MOTIFS ALÉATOIRES ADJACENTS
# ============================================================

def generer_motifs_aleatoires(grille, taille_min=2, taille_max=5):
    """
    Génère des motifs aléatoires avec cases adjacentes orthogonalement.
    Toutes les cases appartiennent à un motif.
    """

    non_assignees = {
        (l, c)
        for l in range(grille.nb_lignes)
        for c in range(grille.nb_colonnes)
    }

    motif_id = 0

    while non_assignees:
        depart = random.choice(list(non_assignees))

        taille_voulue = random.randint(taille_min, taille_max)
        courant = {depart}
        frontiere = set(grille.obtenir_voisins_orthogonaux_coords(*depart)) & non_assignees

        while len(courant) < taille_voulue and frontiere:
            nouvelle = random.choice(list(frontiere))
            courant.add(nouvelle)

            # recalcul de la frontière
            frontiere.remove(nouvelle)

            for voisin in grille.obtenir_voisins_orthogonaux_coords(*nouvelle):
                if voisin in non_assignees and voisin not in courant:
                    frontiere.add(voisin)

        # sécurité : si des cases restantes sont isolées, on accepte des petits motifs
        cases_motif = []
        for l, c in courant:
            cases_motif.append(grille.get_case(l, c))

        motif = Motif(motif_id, cases_motif)
        grille.ajouter_motif(motif)

        for coord in courant:
            non_assignees.remove(coord)

        motif_id += 1


# ============================================================
# RETRAIT DE VALEURS POUR CRÉER LA GRILLE DE DÉPART
# ============================================================

def retirer_valeurs(grille, nb_cases_depart):
    toutes_cases = [
        grille.cases[l][c]
        for l in range(grille.nb_lignes)
        for c in range(grille.nb_colonnes)
    ]

    nb_total = len(toutes_cases)
    nb_a_retirer = nb_total - nb_cases_depart

    if nb_a_retirer <= 0:
        for case in toutes_cases:
            case.fixe = True
        return

    random.shuffle(toutes_cases)

    # on commence par tout mettre en fixe
    for case in toutes_cases:
        case.fixe = True

    # puis on retire certaines valeurs
    for case in toutes_cases[:nb_a_retirer]:
        case.valeur = None
        case.fixe = False


# ============================================================
# CRÉATION COMPLÈTE D'UNE GRILLE
# ============================================================

def creer_grille_jeu(nb_tentatives=100):
    taille = 8
    taille_min_motif = 1
    taille_max_motif = 3
    nb_cases_depart = 12

    for tentative in range(nb_tentatives):
        grille = Grille(taille, taille)

        generer_motifs_aleatoires(grille, taille_min=taille_min_motif, taille_max=taille_max_motif)

        if resoudre(grille):
            grille.solution = grille.copier_valeurs()
            retirer_valeurs(grille, nb_cases_depart)
            return grille

    return None
