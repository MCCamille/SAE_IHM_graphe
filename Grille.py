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
        
        
    # Permet d'obtenir une case de la grille à partir de ses coordonnées (ligne, colonne)
    def get_case(self, ligne, colonne) -> Case:
        return self.cases[ligne][colonne]
    
    
    # Permet de copier les valeurs actuelles de la grille dans une matrice
    def copier_valeurs(self):
        """Renvoie une matrice des valeurs actuelles de la grille, avec None pour les cases vides."""
        
        return [
            [self.cases[l][c].valeur for c in range(self.colonnes)]
            for l in range(self.lignes)
        ]

    # Permet d'obtenir les cases voisines (y compris diagonales) d'une case donnée
    def obtenir_voisins(self, case) -> list:
        """Renvoie les cases voisines (y compris diagonales) d'une case donnée."""
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

    # Permet d'obtenir les coordonnées des cases voisines orthogonales d'une case donnée
    def obtenir_voisins_orthogonaux_coords(self, ligne, colonne) -> list:
        """Renvoie les coordonnées (ligne, colonne) des cases orthogonales voisines (haut, bas, gauche, droite)."""
        voisins = []
        for dl, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nl = ligne + dl
            nc = colonne + dc
            if 0 <= nl < self.lignes and 0 <= nc < self.colonnes:
                voisins.append((nl, nc))
        return voisins

    # Permet d'ajouter un motif à la grille
    def ajouter_motif(self, motif) -> None:
        """Enregistre un motif dans la grille et met à jour les cases concernées."""
        self.motifs[motif.motif_id] = motif
        for case in motif.cases:
            case.id_motif = motif.motif_id

    # Permet de modifier la valeur d'une case si elle n'est pas fixe et que la valeur est valide pour son motif
    def modifier_case(self, ligne, colonne, valeur) -> bool:
        """Modifie la valeur d'une case si elle n'est pas fixe et que la valeur est valide pour son motif.
        Renvoie True si la modification a été effectuée, False sinon."""
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

    # Permet de convertir la grille en un dictionnaire pour la sauvegarde JSON
    def to_dict(self):
        """Convertit la grille en un dictionnaire pour la sauvegarde JSON."""
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

    # Permet de sauvegarder la grille au format JSON
    def sauvegarder_json(self, nom_fichier):
        """Sauvegarde la grille au format JSON."""
        with open(nom_fichier, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, separators=(",", ": "))

    # Permet d'afficher les motifs de la grille
    def afficher_motifs(self):
        """Affiche les motifs de la grille en utilisant les id_motif de chaque case."""
        for l in range(self.lignes):
            # Le :2 force le texte à prendre 2 caractères de large. 
            # Si c'est un seul chiffre, Python ajoute un espace invisible avant.
            print(" ".join(f"{self.cases[l][c].id_motif:2}" for c in range(self.colonnes)))

    # Permet d'afficher les valeurs de la grille
    def afficher_valeurs(self):
        """Affiche les valeurs de la grille, en affichant " ." pour les cases vides pour garder l'alignement."""
        for ligne in self.cases:
            # On vérifie si c.valeur existe. Si oui, on l'affiche sur 2 caractères.
            # Si c'est None, on affiche " ." pour garder le même alignement.
            print(" ".join(f"{c.valeur:2}" if c.valeur is not None else " ." for c in ligne))
    
    #Permet de vérifier si le chiffre peut etre placé dans la grille
    def est_chiffre_valide(self, case, chiffre):
        """Vérifie les 8 voisin pour placer un chiffres dans la grille."""
        ligne_c = case.ligne
        colonne_c = case.colonne

        # On boucle sur les 8 cases autour (y compris diagonales)
        for dl in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dl == 0 and dc == 0:
                    continue
                
                nl = ligne_c + dl
                nc = colonne_c + dc
                
                # Si le voisin est bien dans la grille
                if 0 <= nl < self.lignes and 0 <= nc < self.colonnes:
                    if self.cases[nl][nc].valeur == chiffre:
                        return False # si le meme chiffre est trouvé dans les voisin 
                        
        return True
       
    # Permet de résoudre la grille en comptant le nombre de solutions possibles        
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

        motif = self.motifs[case_vide.id_motif]
        
        # On ne teste que les chiffres valides pour la taille motif (ex: de 1 à 2)
        for ch in range(1, motif.taille + 1):
            
            # pas de doublon dans le motif
            if ch in motif.valeurs_presentes():
                continue
            
            # pas de doublon dans les cases adjacentes
            if not self.est_chiffre_valide(case_vide, ch):
                continue

            case_vide.valeur = ch
            solutions_trouvees = self.resoudre_complet(solutions_trouvees)
            case_vide.valeur = None 

            if solutions_trouvees >= 2:
                break

        return solutions_trouvees
    
    def generer_jeu_parfait(self):
        """
        Génère simultanément les motifs et les chiffres pour garantir 
        une grille valide du premier coup.
        """
        # Réinitialisation de la grille et des motifs
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

            # Si toutes les cases ont un motif, la grille est complète
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
                    continue # Impossible de faire un motif de cette taille
                
                random.shuffle(formes_possibles)

                # Pour chaque forme géométrique trouvée
                for forme in formes_possibles:
                    # Générer toutes les permutations de chiffres de 1 à taille (ex: [1, 3, 2])
                    chiffres_possibles = list(range(1, taille + 1))
                    # On teste quelques permutations aléatoires de chiffres pour cette forme
                    for _ in range(5): # 5 essais de chiffres par forme
                        random.shuffle(chiffres_possibles)
                        
                        # On teste si cette combinaison de chiffres respecte la validité locale (pas de doublons dans les cases adjacentes)
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
                            
                            #On nettoie tout si ça a échoué plus loin
                            del self.motifs[id_motif_actuel]
                            for case_forme in forme:
                                case_forme.id_motif = None
                                case_forme.valeur = None
                                
            return False

        return backtrack(1)