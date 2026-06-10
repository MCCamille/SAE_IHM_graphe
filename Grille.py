import random
import json
from Case import Case
from Motif import Motif

class Grille:
    def __init__(self, l , c):
        self.ligne = l
        self.colonne = c
        # Création de la matrice de cases (de (0,0) à (N-1, N-1))
        self.matrice = [
            [Case(ligne=l, colonne=c) for c in range(self.colonne)]
            for l in range(self.ligne)
        ]
        self.motifs = []  # Pour stocker les motifs créées
                    
    
    #--------------Génération de Motifs----------------

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
            
     # ── Import Json ────────────────────────────
 
    @staticmethod
    def depuis_json(donnees: dict) -> "Grille":
        """
        Crée une Grille depuis un dictionnaire au format :
            { "motif1": [[col, ligne, valeur], ...], ... }
        valeur = 0 signifie case vide.
        La taille est déduite automatiquement.
        """
        max_col = max_ligne = 0
        for cases_json in donnees.values():
            for col, ligne, _ in cases_json:
                max_col   = max(max_col,   col)
                max_ligne = max(max_ligne, ligne)
 
        grille = Grille(nb_lignes=max_ligne + 1, nb_colonnes=max_col + 1)
 
        for index, cases_json in enumerate(donnees.values()):
            cases_motif = []
            for col, ligne, valeur in cases_json:
                case = grille.cases[ligne][col]
                case.id_motif = index
                case.valeur   = valeur if valeur != 0 else None
                cases_motif.append(case)
            grille.motifs.append(Motif(index, cases_motif))
 
        return grille
 
    @staticmethod
    def depuis_fichier_json(chemin: str) -> "Grille":
        """
        Charge depuis un fichier .json.
        Utilise la section "depart" si le fichier contient les deux sections,
        sinon charge directement le dictionnaire racine.
        """
        with open(chemin, encoding="utf-8") as f:
            donnees = json.load(f)
        source = donnees.get("depart", donnees)
        return Grille.depuis_json(source)
 
    # ── Export JSON ───────────────────────────
 
    def vers_json(self) -> dict:
        """
        Exporte la grille dans un dictionnaire avec deux sections :
 
        "depart"
            L'état initial du puzzle : seules les cases bloquées ont une valeur,
            les autres valent 0.
            → PyQt l'utilise pour reconstruire la Grille (Grille.depuis_json)
            → PyQt l'utilise pour savoir quelles cases sont non-modifiables
 
        "actuel"
            L'état en cours : toutes les valeurs posées par le joueur sont incluses,
            les cases vides valent 0.
            → PyQt l'utilise pour pré-remplir les champs de saisie au rechargement
 
        Format de chaque case : [col, ligne, valeur]
        """
        depart: dict[str, list] = {}
        actuel: dict[str, list] = {}
 
        for motif in self.motifs:
            nom = f"motif{motif.id_motif + 1}"
            depart[nom] = []
            actuel[nom] = []
            for case in motif.cases:
                col, ligne = case.colonne, case.ligne
                depart[nom].append([col, ligne, case.valeur if case.bloquee else 0])
                actuel[nom].append([col, ligne, case.valeur if case.valeur is not None else 0])
 
        return {"depart": depart, "actuel": actuel}
 
    def sauvegarder_json(self, chemin: str):
        """Sauvegarde l'état complet (départ + actuel) dans un fichier .json."""
        with open(chemin, "w", encoding="utf-8") as f:
            json.dump(self.vers_json(), f, indent=2, ensure_ascii=False)
 
    def mettre_a_jour_depuis_json(self, donnees_actuel: dict):
        """
        Met à jour les valeurs joueur depuis la section "actuel" du JSON.
        Les cases bloquées sont ignorées.
 
        Utilisation côté PyQt — à appeler après chaque saisie du joueur :
 
            avec open("partie.json") as f:
                donnees = json.load(f)
            grille.mettre_a_jour_depuis_json(donnees["actuel"])
        """
        for cases_json in donnees_actuel.values():
            for col, ligne, valeur in cases_json:
                case = self.cases[ligne][col]
                if not case.bloquee:
                    case.valeur = valeur if valeur != 0 else None
 
            
            
     # ── Actions du joueur ─────────────────────
 
    def poser_valeur(self, ligne: int, colonne: int, valeur: int) -> bool:
        """Pose une valeur. Refuse si case bloquée."""
        case = self.obtenir_case(ligne, colonne)
        if case.bloquee:
            return False
        case.valeur = valeur
        return True
 
    def effacer_case(self, ligne: int, colonne: int) -> bool:
        """Efface une case. Refuse si case bloquée."""
        case = self.obtenir_case(ligne, colonne)
        if case.bloquee:
            return False
        case.valeur = None
        return True
    
    #----------------Regles de jeu---------------- 
    def voisins_valides(self, case: Case) -> bool:
        if case.est_vide():
            return True
        return all(v.valeur != case.valeur for v in self.obtenir_voisins(case))
 
    def cases_en_erreur(self) -> list:
        erreurs = []
        for l in range(self.nb_lignes):
            for c in range(self.nb_colonnes):
                case = self.cases[l][c]
                if case.est_vide():
                    continue
                motif = self.motifs[case.id_motif]
                if case.valeur < 1 or case.valeur > motif.taille:
                    erreurs.append(case)
                elif not self.voisins_valides(case):
                    erreurs.append(case)
        for motif in self.motifs:
            vues: dict[int, list] = {}
            for case in motif.cases:
                if case.valeur is not None:
                    vues.setdefault(case.valeur, []).append(case)
            for liste in vues.values():
                if len(liste) > 1:
                    for case in liste:
                        if case not in erreurs:
                            erreurs.append(case)
        return erreurs
 
    def est_complete(self) -> bool:
        return all(
            not self.cases[l][c].est_vide()
            for l in range(self.nb_lignes)
            for c in range(self.nb_colonnes)
        )
 
    def est_gagnee(self) -> bool:
        return self.est_complete() and len(self.cases_en_erreur()) == 0
 
    
    
    #----------------Affichage de la grille----------------
    
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