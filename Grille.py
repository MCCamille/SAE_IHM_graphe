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
    
    def est_chiffre_valide(self, case, chiffre):
        """Vérifie STRICTEMENT les 8 voisins (Règle du Roi)."""
        ligne_c = case.ligne
        colonne_c = case.colonne

        # On boucle manuellement sur les 8 cases autour (y compris diagonales)
        for dl in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dl == 0 and dc == 0:
                    continue
                
                nl = ligne_c + dl
                nc = colonne_c + dc
                
                # Si le voisin est bien dans la grille
                if 0 <= nl < self.lignes and 0 <= nc < self.colonnes:
                    if self.cases[nl][nc].valeur == chiffre:
                        return False # Doublon trouvé dans les 8 voisins !
                        
        return True

    def remplir_chiffres_seuls(self):
        """Remplit la grille en respectant uniquement la contrainte du Roi."""
        # 1. Trouver la PREMIÈRE case vide
        case_vide = None
        for l in range(self.lignes):
            for c in range(self.colonnes):
                if self.cases[l][c].valeur is None: # Vérification directe
                    case_vide = self.cases[l][c]
                    break
            if case_vide: break

        # Si plus de case vide, la solution est trouvée !
        if not case_vide:
            return True 

        # 2. On teste des chiffres de 1 à 5 mélangés
        chiffres = [1, 2, 3, 4, 5]
        random.shuffle(chiffres)

        for ch in chiffres:
            if self.est_chiffre_valide(case_vide, ch):
                case_vide.valeur = ch # Écriture directe forcée
                
                if self.remplir_chiffres_seuls():
                    return True
                    
                case_vide.valeur = None # Backtrack propre

        return False

    def generer_motifs_depuis_chiffres(self):
        """
        Crée des dominos (motifs de taille 2) en associant une case impaire 
        avec une case paire voisine. Simple, rapide et sans aucun doublon possible.
        """
        self.motifs = {}
        for ligne in self.cases:
            for case in ligne:
                case.id_motif = None

        cases_sans_motif = [c for ligne in self.cases for c in ligne]
        random.shuffle(cases_sans_motif)
        
        id_actuel = 1

        while cases_sans_motif:
            case_depart = cases_sans_motif.pop(0)
            
            # On va chercher un voisin orthogonal libre pour faire un motif de taille 2
            extensions_possibles = []
            for nl, nc in self.obtenir_voisins_orthogonaux_coords(case_depart.ligne, case_depart.colonne):
                voisin = self.cases[nl][nc]
                
                # Pour que le motif de taille 2 soit valide, il faut :
                # 1. Que le voisin n'ait pas de motif
                # 2. Que son chiffre soit différent de notre case de départ
                if voisin.id_motif is None and voisin.valeur != case_depart.valeur:
                    extensions_possibles.append(voisin)
            
            if extensions_possibles:
                # On a trouvé un voisin valide -> Motif de taille 2 !
                choix = random.choice(extensions_possibles)
                cases_motif = [case_depart, choix]
                choix.id_motif = id_actuel
                case_depart.id_motif = id_actuel
                if choix in cases_sans_motif:
                    cases_sans_motif.remove(choix)
            else:
                # Si la case est totalement isolée par d'autres motifs, 
                # on en fait un motif de taille 1 (il ne contient que son propre chiffre).
                # Règle de cohérence : un motif de taille 1 ne peut contenir que le chiffre 1.
                # Donc on force sa valeur à 1 pour que la grille reste résolvable.
                cases_motif = [case_depart]
                case_depart.valeur = 1
                case_depart.id_motif = id_actuel

            # Enregistrement du motif
            nouveau_motif = Motif(id_actuel, cases_motif)
            self.ajouter_motif(nouveau_motif)
            id_actuel += 1
                
    def resoudre_complet(self, solutions_trouvees=0):
        if solutions_trouvees >= 2:
            return solutions_trouvees

        case_vide = None
        for l in range(self.lignes):
            for c in range(self.colonnes):
                if self.cases[l][c].est_vide():
                    case_vide = self.cases[l][c]
                    break
            if case_vide: break

        if not case_vide:
            return solutions_trouvees + 1

        # C'EST ICI QUE ÇA CHANGE :
        motif = self.motifs[case_vide.id_motif]
        
        # On ne teste QUE les chiffres valides pour la taille de CE motif (ex: de 1 à 2)
        for ch in range(1, motif.taille + 1):
            
            # Règle 1 : Pas de doublon dans le motif
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
    
    import random

    def generer_jeu_parfait(self):
        """
        Génère simultanément les motifs et les chiffres pour garantir 
        une grille 100% valide du premier coup.
        """
        # Réinitialisation propre
        self.motifs = {}
        for ligne in self.cases:
            for case in ligne:
                case.id_motif = None
                case.valeur = None

        def backtrack(id_motif_actuel):
            # Trouver la première case qui n'a pas encore de motif
            case_libre = None
            for l in range(self.lignes):
                for c in range(self.colonnes):
                    if self.cases[l][c].id_motif is None:
                        case_libre = self.cases[l][c]
                        break
                if case_libre: break

            # Si toutes les cases ont un motif, la grille est finie et parfaite !
            if not case_libre:
                return True

            # On teste des tailles de motifs de 1 à 5 au hasard
            tailles = [1, 2, 3, 4, 5]
            random.shuffle(tailles)

            for taille in tailles:
                # On va essayer de construire un motif de cette taille à partir de case_libre
                formes_possibles = []
                
                # Algorithme pour trouver des combinaisons de cases adjacentes libres
                def trouver_formes(cases_actuelles, taille_visee):
                    if len(cases_actuelles) == taille_visee:
                        formes_possibles.append(list(cases_actuelles))
                        return
                    for c in cases_actuelles:
                        for nl, nc in self.obtenir_voisins_orthogonaux_coords(c.ligne, c.colonne):
                            v = self.cases[nl][nc]
                            if v.id_motif is None and v not in cases_actuelles:
                                trouver_formes(cases_actuelles + [v], taille_visee)

                trouver_formes([case_libre], taille)
                
                if not formes_possibles:
                    continue # Impossible de faire un motif de cette taille ici
                
                random.shuffle(formes_possibles)

                # Pour chaque forme géométrique trouvée
                for forme in formes_possibles:
                    # Générer toutes les permutations de chiffres de 1 à taille (ex: [1, 3, 2])
                    chiffres_possibles = list(range(1, taille + 1))
                    # On teste quelques permutations aléatoires de chiffres pour cette forme
                    for _ in range(5): # 5 essais de chiffres par forme pour aller vite
                        random.shuffle(chiffres_possibles)
                        
                        # On teste si cette combinaison de chiffres respecte la règle du Roi
                        valide = True
                        for i, case_forme in enumerate(forme):
                            if not self.est_chiffre_valide(case_forme, chiffres_possibles[i]):
                                valide = False
                                break
                        
                        if valide:
                            # On applique temporairement le motif et les chiffres
                            for i, case_forme in enumerate(forme):
                                case_forme.id_motif = id_motif_actuel
                                case_forme.valeur = chiffres_possibles[i]
                            
                            # On crée l'objet Motif pour le solveur
                            from Motif import Motif
                            mon_motif = Motif(id_motif_actuel, forme)
                            self.ajouter_motif(mon_motif)

                            # Appel récursif pour la suite de la grille
                            if backtrack(id_motif_actuel + 1):
                                return True
                            
                            # Backtrack : On nettoie tout si ça a échoué plus loin
                            del self.motifs[id_motif_actuel]
                            for case_forme in forme:
                                case_forme.id_motif = None
                                case_forme.valeur = None
                                
            return False

        return backtrack(1)