from Grille import Grille
from Motif import Motif
from Case import Case
import random

def prochaine_case_vide(grille) -> Case:
    meilleure_case = None
    meilleur_nb = None

    for l in range(grille.lignes):
        for c in range(grille.colonnes):
            case = grille.cases[l][c]
            if case.est_vide():
                nb_possibles = len(valeurs_possibles(grille, case))

                if nb_possibles == 0:
                    return None  # ← signale échec immédiat au solveur

                if meilleur_nb is None or nb_possibles < meilleur_nb:
                    meilleure_case = case
                    meilleur_nb = nb_possibles

    return meilleure_case


def valeurs_possibles(grille, case):
    motif = grille.motifs[case.id_motif]

    deja_dans_motif = {
    c.valeur for c in motif.cases
    if c.valeur is not None and c != case  # ← exclure la case courante
}
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
    
    possibles = valeurs_possibles(grille, case)

    for valeur in valeurs_possibles(grille, case):
        case.valeur = valeur
        if resoudre(grille):
            return True
        case.valeur = None
    return False


def generer_motifs_aleatoires(grille, taille_min=1, taille_max=5):
    non_assignees = {
        (l, c)
        for l in range(grille.lignes)
        for c in range(grille.colonnes)
    }

    motif_id = 0

    while non_assignees:
        depart = min(non_assignees)
        reste = len(non_assignees)

        taille_voulue = random.randint(taille_min, taille_max)
        taille_voulue = min(taille_voulue, reste)

        courant = {depart}
        frontiere = set()

        for voisin in grille.obtenir_voisins_orthogonaux_coords(*depart):
            if voisin in non_assignees:
                frontiere.add(voisin)

        while len(courant) < taille_voulue and frontiere:
            nouvelle = random.choice(list(frontiere))
            frontiere.remove(nouvelle)

            if nouvelle not in non_assignees or nouvelle in courant:
                continue

            courant.add(nouvelle)

            for voisin in grille.obtenir_voisins_orthogonaux_coords(*nouvelle):
                if voisin in non_assignees and voisin not in courant:
                    frontiere.add(voisin)

        cases_motif = [grille.get_case(l, c) for (l, c) in courant]
        motif = Motif(motif_id, cases_motif)
        grille.ajouter_motif(motif)

        for coord in courant:
            non_assignees.remove(coord)

        motif_id += 1

def retirer_valeurs(grille, nb_cases_depart):
    toutes_cases = [
        grille.cases[l][c]
        for l in range(grille.lignes)
        for c in range(grille.colonnes)
    ]

    # tout mettre en fixe
    for case in toutes_cases:
        case.fixe = True

    cases_retirables = []
    for motif in grille.motifs.values():
        cases_motif = list(motif.cases)
        random.shuffle(cases_motif)
        
        # garder entre 1 et 2 cases par motif (aléatoirement)
        nb_a_garder = random.randint(1, min(2, len(cases_motif)))
        cases_retirables.extend(cases_motif[nb_a_garder:])

    # mélanger retirer jusqu'à atteindre nb_cases_depart
    random.shuffle(cases_retirables)
    nb_total = len(toutes_cases)
    nb_a_retirer = nb_total - nb_cases_depart

    for case in cases_retirables[:nb_a_retirer]:
        case.valeur = None
        case.fixe = False


def creer_grille_jeu(taille=8, nb_cases_depart=12, taille_min_motif=2, taille_max_motif=5, nb_tentatives=100):
    for tentative in range(nb_tentatives):
        print(f"Tentative {tentative + 1}...")
        grille = Grille(taille, taille)
        generer_motifs_aleatoires(grille, taille_min=taille_min_motif, taille_max=taille_max_motif)
        if resoudre(grille):
            print("Grille résolue !")
            grille.solution = grille.copier_valeurs()
            retirer_valeurs(grille, nb_cases_depart)
            return grille
        else:
            print("Échec de résolution")
    return None