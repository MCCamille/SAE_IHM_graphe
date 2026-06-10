import random
from Case import Case
from Motif import Motif

class Grille:
    def __init__(self, l , c):
        self.ligne = l
        self.colonne = c
        # Création de la matrice de cases (de (0,0) à (N-1, N-1))
        self.matrice = [
            [Case(ligne=l, colonne=c, valeur=0, fixe=False) for c in range(self.colonne)]
            for l in range(self.ligne)
        ]
        self.motifs = []  # Pour stocker les motifs créées

    def obtenir_voisins_libres(self, case):
        voisins = []
        # Directions : Haut, Bas, Gauche, Droite
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dl, dc in directions:
            nl, nc = case.ligne + dl, case.colonne + dc
            # Vérification des limites de la grille
            if 0 <= nl < self.ligne and 0 <= nc < self.colonne:
                voisin = self.matrice[nl][nc]
                # On ne prend que les cases qui n'ont pas encore de motif
                if voisin.id_motif is None:
                    voisins.append(voisin)
        return voisins

<<<<<<< HEAD
    def definir_motifs(self, motif_map: list[list[int]]):
        motifs_dict: dict[int, list[Case]] = {}
        for r in range(self.lignes):
            for c in range(self.colonnes):
                sid = motif_map[r][c]
                self.cases[r][c].motif_id = sid
                motifs_dict.setdefault(sid, []).append(self.cases[r][c])

        self.motifs = [
            Motif(sid, cases) for sid, cases in motifs_dict.items()
        ]

    def placer_valeur_initiale(self, ligne: int, colonne: int, valeur: int):
        case = self.get_case(ligne, colonne)
        case.valeur = valeur
        case.fixe = True  # case impossible à modifier pour le joueur
=======
    def generer_tous_les_motifs(self):
        id_actuel = 1
        
        # Créer une liste à plat de toutes les cases non attribuées
        cases_libres = []
        for ligne in self.matrice:
            for case in ligne:
                cases_libres.append(case)
        
        # Boucle principale tant qu'il reste des cases à attribuer
        while len(cases_libres) > 0:
            # Choisir une case de départ au hasard
            case_depart = random.choice(cases_libres)
            cases_libres.remove(case_depart)
            
            # Initialiser le motif en cours
            case_depart.id_motif = id_actuel
            cases_du_motif = [case_depart]
            
            taille_cible = random.randint(1, 5)
            
            # Recherche des voisins disponibles initiaux
            candidats_voisins = self.obtenir_voisins_libres(case_depart)
            
            # La boucle continue UNIQUEMENT si on n'a pas atteint la taille ET qu'il reste des voisins
            while len(cases_du_motif) < taille_cible and len(candidats_voisins) > 0:
                # Choisir un voisin au hasard
                prochaine_case = random.choice(candidats_voisins)
                
                # Assigner le motif et mettre à jour les listes
                prochaine_case.id_motif = id_actuel
                cases_du_motif.append(prochaine_case)
                cases_libres.remove(prochaine_case)
                
                # Recalculer les voisins libres pour l'ensemble des cases du motif actuel
                nouveaux_candidats = set()
                for c in cases_du_motif:
                    for v in self.obtenir_voisins_libres(c):
                        nouveaux_candidats.add(v)
                candidats_voisins = list(nouveaux_candidats)
            
            # Enregistrer le motif finalisé dans notre liste
            nouveau_motif = Motif(motif_id=id_actuel, cases=cases_du_motif)
            self.motifs.append(nouveau_motif)
            
            id_actuel += 1
            
            
    def afficher(self):
        print("GRILLE (ID MOTIFS)")
        for ligne in self.matrice:
            ligne_texte = []
            for case in ligne:
                if case.id_motif is None:
                    ligne_texte.append(" . ")
                else:
                    ligne_texte.append(f"{case.id_motif:02d}")
            
            print(" ".join(ligne_texte))
        
        
        
Grille_test = Grille(8,8)
Grille_test.generer_tous_les_motifs()
Grille_test.afficher()
>>>>>>> 0effd86d842b435876f55e15383699573c454ad3
