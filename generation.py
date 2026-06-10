from Grille import Grille
from Motif import Motif
from Case import Case
import random


def prochaine_case_vide(grille) -> Case:
    meilleure_case = None
    meilleur_nb = None

    for l in range(grille.nb_lignes):
        for c in range(grille.nb_colonnes):
            case = grille.cases[l][c]
            if case.est_vide():
                nb_possibles = len(valeurs_possibles(grille, case))

                if nb_possibles == 0:
                    return case

                if meilleur_nb is None or nb_possibles < meilleur_nb:
                    meilleure_case = case
                    meilleur_nb = nb_possibles

    return meilleure_case


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

def generer_motifs_aleatoires(grille, taille_min=1, taille_max=5):
    """
    Génération semi-aléatoire plus stable :
    - motifs adjacents orthogonalement
    - tailles entre 1 et 5
    - on évite de laisser trop de petites zones isolées
    """

    non_assignees = {
        (l, c)
        for l in range(grille.nb_lignes)
        for c in range(grille.nb_colonnes)
    }

    motif_id = 0

    while non_assignees:
        # on prend toujours une case "ordonnée" pour éviter le chaos total
        depart = min(non_assignees)

        reste = len(non_assignees)

        # on évite de demander un motif plus grand que ce qu'il reste
        taille_voulue = random.randint(taille_min, taille_max)
        taille_voulue = min(taille_voulue, reste)

        courant = {depart}
        frontiere = set()

        for voisin in grille.obtenir_voisins_orthogonaux_coords(*depart):
            if voisin in non_assignees:
                frontiere.add(voisin)

        while len(courant) < taille_voulue and frontiere:
            # on prend un voisin au hasard parmi la frontière
            nouvelle = random.choice(list(frontiere))
            frontiere.remove(nouvelle)

            if nouvelle not in non_assignees or nouvelle in courant:
                continue

            courant.add(nouvelle)

            for voisin in grille.obtenir_voisins_orthogonaux_coords(*nouvelle):
                if voisin in non_assignees and voisin not in courant:
                    frontiere.add(voisin)

        # création du motif
        cases_motif = [grille.get_case(l, c) for (l, c) in courant]
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
    taille_max_motif = 5
    nb_cases_depart = 12

    for tentative in range(nb_tentatives):
        grille = Grille(taille, taille)

        generer_motifs_aleatoires(
            grille,
            taille_min=taille_min_motif,
            taille_max=taille_max_motif
        )

        if resoudre(grille):
            grille.solution = grille.copier_valeurs()
            retirer_valeurs(grille, nb_cases_depart)
            return grille

    return None
