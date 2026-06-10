import json
from Case import Case
from Motif import Motif

class Grille:
    def __init__(self, lignes, colonnes):
        self.lignes = lignes 
        self.colonnes = colonnes
        self.cases = [[Case(l, c) for c in range(colonnes)] for l in range(lignes)]
        self.motifs = {}

    def get_case(self, ligne, colonne) -> Case:
        return self.cases[ligne][colonne]
    
    def copier_valeurs(self):
        return [
            [self.cases[l][c].valeur for c in range(self.colonnes)]
            for l in range(self.lignes)
        ]

    def obtenir_voisins(self, case) -> list:
        voisins = []
        for dl in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dl == 0 and dc == 0:
                    continue
                nl = case.ligne + dl
                nc = case.colonne + dc
                if 0 <= nl < self.lignes and 0 <= nc < self.colonnes:
                    voisins.append(self.cases[nl][nc])
        return voisins

    def obtenir_voisins_orthogonaux_coords(self, ligne, colonne) -> list:
        voisins = []
        for dl, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nl = ligne + dl
            nc = colonne + dc
            if 0 <= nl < self.lignes and 0 <= nc < self.colonnes:
                voisins.append((nl, nc))
        return voisins

    def ajouter_motif(self, motif) -> None:
        self.motifs[motif.motif_id] = motif
        for case in motif.cases:
            case.id_motif = motif.motif_id

    def modifier_case(self, ligne, colonne, valeur) -> bool:
        case = self.cases[ligne][colonne]
        if case.fixe:
            return False
        if valeur is None:
            case.valeur = None
            return True
        motif = self.motifs[case.id_motif]
        if 1 <= valeur <= motif.taille:
            case.valeur = valeur
            return True
        return False

    def to_dict(self):
        # Remplacement de motif_id par id_motif ici :
        motif_map = [
            [self.cases[r][c].id_motif for c in range(self.colonnes)]
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

    def afficher_motifs(self):
        for l in range(self.lignes):
            # Le :2 force le texte à prendre 2 caractères de large. 
            # Si c'est un seul chiffre, Python ajoute un espace invisible avant.
            print(" ".join(f"{self.cases[l][c].id_motif:2}" for c in range(self.colonnes)))

    def afficher_valeurs(self):
        for ligne in self.cases:
            # On applique la même logique pour les valeurs pour que les deux grilles soient identiques visuellement
            print(" ".join(f"{case.valeur:2}" if case.valeur is not None else " ." for case in ligne))