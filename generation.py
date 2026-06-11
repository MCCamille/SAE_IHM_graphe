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
        return True  # ← aucune case vide = grille complète

    possibles = valeurs_possibles(grille, case)
    if len(possibles) == 0:
        return False  # ← case bloquée = échec, on backtrack

    for valeur in possibles:
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
    # Étape 1 : remettre toutes les valeurs depuis la solution
    for l in range(grille.lignes):
        for c in range(grille.colonnes):
            grille.cases[l][c].valeur = grille.solution[l][c]
            grille.cases[l][c].fixe = False

    # Étape 2 : garantir 1 case visible par motif via coordonnées
    ids_gardes = set()
    for motif in grille.motifs.values():
        # Récupérer les coordonnées des cases du motif
        coords = [(case.ligne, case.colonne) for case in motif.cases]
        l, c = random.choice(coords)
        ids_gardes.add((l, c))

    # Étape 3 : compléter jusqu'à nb_cases_depart
    toutes_coords = [
        (l, c)
        for l in range(grille.lignes)
        for c in range(grille.colonnes)
        if (l, c) not in ids_gardes
    ]
    random.shuffle(toutes_coords)
    nb_manquantes = nb_cases_depart - len(ids_gardes)
    for coord in toutes_coords[:max(0, nb_manquantes)]:
        ids_gardes.add(coord)

    # Étape 4 : fixer ou effacer
    for l in range(grille.lignes):
        for c in range(grille.colonnes):
            case = grille.cases[l][c]
            if (l, c) in ids_gardes:
                case.fixe = True
            else:
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
            print("Solution :")
            for ligne in grille.solution:
                print(ligne)
            retirer_valeurs(grille, nb_cases_depart)
            print("Après retirer_valeurs :")
            for l in range(grille.lignes):
                print([grille.cases[l][c].valeur for c in range(grille.colonnes)])
            return grille
        else:
            print("Échec de résolution")
    return None