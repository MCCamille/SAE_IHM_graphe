import json
import random
from Case import Case
from Motif import Motif

class Grille:
    def __init__(self, nb_lignes, nb_colonnes):
        self.nb_lignes = nb_lignes
        self.nb_colonnes = nb_colonnes

        self.cases = [
            [Case(l, c) for c in range(nb_colonnes)]
            for l in range(nb_lignes)
        ]

        self.motifs = {}
        self.solution = None  # sera stockée après résolution

    def get_case(self, ligne, colonne):
        return self.cases[ligne][colonne]

    def obtenir_voisins(self, case):
        voisins = []

        for dl in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dl == 0 and dc == 0:
                    continue

                nl = case.ligne + dl
                nc = case.colonne + dc

                if 0 <= nl < self.nb_lignes and 0 <= nc < self.nb_colonnes:
                    voisins.append(self.cases[nl][nc])

        return voisins

    def obtenir_voisins_orthogonaux_coords(self, ligne, colonne):
        voisins = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dl, dc in directions:
            nl = ligne + dl
            nc = colonne + dc
            if 0 <= nl < self.nb_lignes and 0 <= nc < self.nb_colonnes:
                voisins.append((nl, nc))

        return voisins

    def ajouter_motif(self, motif):
        self.motifs[motif.motif_id] = motif
        for case in motif.cases:
            case.id_motif = motif.motif_id

    def peut_placer(self, case, valeur):
        # la valeur doit être entre 1 et la taille du motif
        motif = self.motifs[case.id_motif]
        if not (1 <= valeur <= motif.taille):
            return False

        # pas de doublon dans le motif
        for autre in motif.cases:
            if autre != case and autre.valeur == valeur:
                return False

        # pas de doublon chez les voisins (8 directions)
        for voisin in self.obtenir_voisins(case):
            if voisin != case and voisin.valeur == valeur:
                return False

        return True

    def modifier_case(self, ligne, colonne, valeur):
        case = self.cases[ligne][colonne]

        if case.fixe:
            return False

        if valeur is None:
            case.valeur = None
            return True

        if self.peut_placer(case, valeur):
            case.valeur = valeur
            return True

        return False

    def copier_valeurs(self):
        return [
            [self.cases[l][c].valeur for c in range(self.nb_colonnes)]
            for l in range(self.nb_lignes)
        ]

    def charger_valeurs(self, matrice):
        for l in range(self.nb_lignes):
            for c in range(self.nb_colonnes):
                self.cases[l][c].valeur = matrice[l][c]

    def to_dict(self):
        # Matrice des motif_id
        motif_map = [
            [self.cases[r][c].motif_id for c in range(self.colonnes)]
            for r in range(self.lignes)
        ]
        
        valeurs_initiales = []
        for r in range(self.lignes):
            for c in range(self.colonnes):
                case = self.cases[r][c]
                if case.fixe and case.valeur is not None:
                    valeurs_initiales.append({
                        "ligne": r,
                        "colonne": c,
                        "valeur": case.valeur
                    })
        
        return {
            "lignes": self.lignes,
            "colonnes": self.colonnes,
            "motifs": motif_map,
            "valeurs_initiales": valeurs_initiales
        }

    def sauvegarder_json(self, nom_fichier):
        with open(nom_fichier, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, separators=(",", ": "))

    def afficher_valeurs(self):
        for ligne in self.cases:
            print(" ".join(str(case.valeur) if case.valeur is not None else "." for case in ligne))

    def afficher_motifs(self):
        for l in range(self.nb_lignes):
            ligne = []
            for c in range(self.nb_colonnes):
                ligne.append(str(self.cases[l][c].id_motif))
            print(" ".join(ligne))


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


# GÉNÉRATION DES MOTIFS ALÉATOIRES ADJACENTS

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


# RETRAIT DE VALEURS POUR CRÉER LA GRILLE DE DÉPART

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


# CRÉATION COMPLÈTE D'UNE GRILLE

def creer_grille_jeu(taille, nb_cases_depart, taille_min_motif=2, taille_max_motif=5, nb_tentatives=30):
    """
    Essaie plusieurs fois de générer une grille solvable.
    """

    for tentative in range(nb_tentatives):
        grille = Grille(taille, taille)

        generer_motifs_aleatoires(grille, taille_min=taille_min_motif, taille_max=taille_max_motif)

        if resoudre(grille):
            grille.solution = grille.copier_valeurs()
            retirer_valeurs(grille, nb_cases_depart)
            return grille

    return None