import json
from Case import Case
from Motif import Motif

class Grille:
    def __init__(self, nb_lignes, nb_colonnes):
        self.nb_lignes = nb_lignes 
        self.nb_colonnes = nb_colonnes
        self.cases = [[Case(l, c) for c in range(nb_colonnes)]for l in range(nb_lignes) ]# matrice de cases de la grille
        self.motifs = {}

    # Renvoie la case à la position donnée
    def get_case(self, ligne, colonne)->Case:
        return self.cases[ligne][colonne]
    
    def copier_valeurs(self):
        return [
            [self.cases[l][c].valeur for c in range(self.nb_colonnes)]
            for l in range(self.nb_lignes)
        ]

    # Renvoie les cases voisines (8 directions) de la case donnée (ou None si hors limites)
    def obtenir_voisins(self, case)->list:
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

    # Renvoie les coordonnées des cases voisines orthogonalement (4 directions) de la position donnée (pour la génération de motifs)
    def obtenir_voisins_orthogonaux_coords(self, ligne, colonne)->list:
        voisins = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dl, dc in directions:
            nl = ligne + dl
            nc = colonne + dc
            if 0 <= nl < self.nb_lignes and 0 <= nc < self.nb_colonnes:
                voisins.append((nl, nc))
        return voisins

    #Ajoute un motif à la grille et met à jour les cases concernées
    def ajouter_motif(self, motif)->None:
        self.motifs[motif.motif_id] = motif
        for case in motif.cases:
            case.id_motif = motif.motif_id

    # Modifie la valeur d'une case si elle n'est pas fixe et que la valeur est valide pour son motif
    def modifier_case(self, ligne, colonne, valeur)->bool:
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
        data = {}
        for i, motif in enumerate(self.motifs.values(), start=1):
            nom_motif = f"motif{i}"
            data[nom_motif] = []
            for case in motif.cases:
                valeur = case.valeur if case.valeur is not None else 0
                data[nom_motif].append([case.colonne, case.ligne, valeur])
        return data


    # Sauvegarde la grille au format JSON
    def sauvegarder_json(self, nom_fichier):
        with open(nom_fichier, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, separators=(",", ": "))

    # Affiche les valeurs de la grille
    def afficher_valeurs(self):
        for ligne in self.cases:
            print(" ".join(str(case.valeur) if case.valeur is not None else "." for case in ligne))

    # Affiche les ids des motifs de la grille
    def afficher_motifs(self):
        for l in range(self.nb_lignes):
            ligne = []
            for c in range(self.nb_colonnes):
                ligne.append(str(self.cases[l][c].id_motif))
            print(" ".join(ligne))