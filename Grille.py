import json
import random
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
            # On vérifie si c.valeur existe. Si oui, on l'affiche sur 2 caractères.
            # Si c'est None, on affiche " ." pour garder le même alignement.
            print(" ".join(f"{c.valeur:2}" if c.valeur is not None else " ." for c in ligne))
    
    # --- À RAJOUTER DANS TA CLASSE GRILLE ---
    def est_chiffre_valide(self, case, chiffre):
        """Vérifie uniquement la règle du Roi (les 8 voisins)."""
        for voisin in self.obtenir_voisins(case):
            if voisin.valeur == chiffre:
                return False
        return True

    def remplir_chiffres_seuls(self):
        """Remplit la grille en respectant uniquement la contrainte du Roi."""
        # Trouver la première case vide
        case_vide = None
        for l in range(self.lignes):
            for c in range(self.colonnes):
                if self.cases[l][c].est_vide():
                    case_vide = self.cases[l][c]
                    break
            if case_vide: break

        if not case_vide:
            return True # Toutes les cases ont un chiffre !

        # On teste des chiffres de 1 à 5 au hasard
        chiffres = [1, 2, 3, 4, 5]
        random.shuffle(chiffres)

        for ch in chiffres:
            if self.est_chiffre_valide(case_vide, ch):
                case_vide.valeur = ch
                if self.remplir_chiffres_seuls():
                    return True
                case_vide.valeur = None # Backtrack

        return False

    def generer_motifs_depuis_chiffres(self):
        """Regroupe les cases en motifs de tailles 1 à 5 sans doublons de chiffres."""
        # On liste toutes les cases qui n'ont pas encore de motif
        cases_sans_motif = [c for ligne in self.cases for c in ligne if c.id_motif is None]
        random.shuffle(cases_sans_motif)
        
        id_actuel = 1

        while cases_sans_motif:
            # On prend une case de départ pour notre nouveau motif
            case_depart = cases_sans_motif.pop(0)
            taille_cible = random.randint(1, 5) # Taille du motif désirée
            
            cases_motif = [case_depart]
            valeurs_motif = {case_depart.valeur}

            # On essaie d'agrandir le motif avec des cases orthogonales voisines
            for _ in range(taille_cible - 1):
                extensions_possibles = []
                for c in cases_motif:
                    for nl, nc in self.obtenir_voisins_orthogonaux_coords(c.ligne, c.colonne):
                        voisin = self.cases[nl][nc]
                        # La case doit être libre et son chiffre ne doit pas être déjà dans le motif
                        if voisin.id_motif is None and voisin not in cases_motif:
                            if voisin.valeur not in valeurs_motif:
                                extensions_possibles.append(voisin)
                
                if not extensions_possibles:
                    break # On ne peut plus l'agrandir, tant pis
                    
                choix = random.choice(extensions_possibles)
                cases_motif.append(choix)
                valeurs_motif.add(choix.valeur)
                if choix in cases_sans_motif:
                    cases_sans_motif.remove(choix)

            # On crée le motif officiel avec les cases trouvées
            nouveau_motif = Motif(id_actuel, cases_motif)
            self.ajouter_motif(nouveau_motif)
            id_actuel += 1
            
            
    def resoudre_complet(self, solutions_trouvees=0):
        """Tente de résoudre la grille et renvoie le nombre de solutions trouvées (max 2)."""
        # Si on a déjà trouvé 2 solutions, inutile de continuer, la grille est ambiguë
        if solutions_trouvees >= 2:
            return solutions_trouvees

        # Trouver la case vide la plus contrainte (MRV simple : première vide)
        case_vide = None
        for l in range(self.lignes):
            for c in range(self.colonnes):
                if self.cases[l][c].est_vide():
                    case_vide = self.cases[l][c]
                    break
            if case_vide: break

        # Si plus aucune case n'est vide, on a trouvé une solution valide !
        if not case_vide:
            return solutions_trouvees + 1

        motif = self.motifs[case_vide.id_motif]
        
        # On teste les chiffres valides pour ce motif
        for ch in range(1, motif.taille + 1):
            # Règle 1 : Pas le même chiffre dans le motif
            if ch in motif.valeurs_presentes():
                continue
            
            # Règle 2 : Règle du Roi (les 8 voisins)
            if not self.est_chiffre_valide(case_vide, ch):
                continue

            # Le chiffre est valide, on tente le coup
            case_vide.valeur = ch
            solutions_trouvees = self.resoudre_complet(solutions_trouvees)
            case_vide.valeur = None # Backtrack

            if solutions_trouvees >= 2:
                break

        return solutions_trouvees