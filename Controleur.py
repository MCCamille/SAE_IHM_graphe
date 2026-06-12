import json
import os
from PyQt6.QtCore import QTimer
from Vue import EcranAccueil, FenetreJeu, PopUpVictoire

FICHIER_SAUVEGARDE = "save_partie.json"
FICHIER_GRILLE = "grille_sudoku.json"
FICHIER_SOLUTION = "solution_grille_sudoku.json"

class Controleur:
    def __init__(self):
        self.chemin_json = FICHIER_GRILLE
        self.nom_joueur = "Player 1"
        self.score = 0
        self.secondes = 0
        self.case_valeur_joueur = {}

        self._timer = QTimer()
        self._timer.timeout.connect(self._tick)

        self.ecran_accueil = None
        self.fenetre_jeu = None
        self.popup_victoire = None

    def demarrer_application(self):
        self.ecran_accueil = EcranAccueil(self)
        self.ecran_accueil.show()

    def nouvelle_partie(self):
        import main as generateur_main
        try:
            generateur_main.main()
        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self.ecran_accueil, "Erreur de génération", f"Impossible de générer une nouvelle grille :\n{e}")
            return

        if os.path.exists(FICHIER_SAUVEGARDE):
            os.remove(FICHIER_SAUVEGARDE)

        self.nom_joueur = "Player 1"
        self.score = 0
        self.secondes = 0
        self.case_valeur_joueur.clear()

        # Si la popup de victoire était ouverte, on la ferme
        if self.popup_victoire:
            self.popup_victoire.close()

        self.fenetre_jeu = FenetreJeu(self.chemin_json, self)
        self._rafraichir_vue()
        
        self.fenetre_jeu.show()
        self.ecran_accueil.close()
        self._timer.start(1000)

    def charger_derniere_partie(self):
        if not os.path.exists(FICHIER_SAUVEGARDE):
            return

        try:
            with open(FICHIER_SAUVEGARDE, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            self.chemin_json = data.get("grille_path", FICHIER_GRILLE)
            self.nom_joueur = data.get("nom_joueur", "Player 1")
            self.score = data.get("score", 0)
            self.secondes = data.get("secondes", 0)
            
            self.case_valeur_joueur.clear()
            for cle, val in data.get("cases_joueur", {}).items():
                x, y = map(int, cle.split(","))
                self.case_valeur_joueur[(x, y)] = val

            self.fenetre_jeu = FenetreJeu(self.chemin_json, self)
            self._rafraichir_vue()
            
            self.fenetre_jeu.show()
            self.ecran_accueil.close()

            if data.get("pause", False):
                self._timer.stop()
            else:
                self._timer.start(1000)

        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self.ecran_accueil, "Erreur", f"Impossible de charger la partie précédente :\n{e}")

    def verifier_grille(self):
        if not os.path.exists(FICHIER_SOLUTION):
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self.fenetre_jeu, "Vérification", f"Le fichier de solution '{FICHIER_SOLUTION}' est introuvable.")
            return

        try:
            with open(FICHIER_SOLUTION, encoding="utf-8") as f:
                data_solution = json.load(f)
            
            solution = {}
            for nom_bloc, cases in data_solution.items():
                for x, y, val in cases:
                    solution[(x, y)] = val

            erreurs = []
            reussite = True

            for y in range(8):
                for x in range(8):
                    val_solution = solution.get((x, y), 0)
                    val_fixe = self.fenetre_jeu.zone_jeu.case_valeur_fixe.get((x, y), 0)
                    val_joueur = self.case_valeur_joueur.get((x, y), None)

                    if val_fixe == 0:
                        if val_joueur is None:
                            reussite = False
                        elif val_joueur != val_solution:
                            erreurs.append((x, y))
                            reussite = False

            if erreurs:
                self.fenetre_jeu.zone_jeu.highlight_erreurs(erreurs)
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.warning(self.fenetre_jeu, "Vérification", f"La grille contient {len(erreurs)} erreur(s). Elles sont affichées en rouge.")
            elif reussite:
                self._timer.stop()
                # On affiche la pop-up personnalisée avec le GIF
                self.popup_victoire = PopUpVictoire(self.nom_joueur, self.score, self)
                self.popup_victoire.show()
            else:
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.information(self.fenetre_jeu, "Vérification", "Pas d'erreurs pour le moment, mais la grille n'est pas complète !")

        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self.fenetre_jeu, "Erreur", f"Erreur lors de la vérification :\n{e}")

    def _rafraichir_vue(self):
        if not self.fenetre_jeu:
            return
        self.fenetre_jeu.maj_nom(self.nom_joueur)
        self.fenetre_jeu.maj_score(self.score)
        m, s = divmod(self.secondes, 60)
        self.fenetre_jeu.maj_timer(f"{m:02d}:{s:02d}")
        self.fenetre_jeu.maj_grille_joueur(self.case_valeur_joueur)

    def appliquer_nom(self, nom):
        self.nom_joueur = nom.strip() or "Player 1"
        if self.fenetre_jeu:
            self.fenetre_jeu.maj_nom(self.nom_joueur)
        self.sauvegarde_auto()

    def modifier_valeur_case(self, x, y, valeur):
        if valeur is None:
            self.case_valeur_joueur.pop((x, y), None)
        else:
            self.case_valeur_joueur[(x, y)] = valeur
        
        self.score = len(self.case_valeur_joueur) * 10
        self._rafraichir_vue()
        self.sauvegarde_auto()

    def reset(self, nom):
        self.nom_joueur = nom.strip() or "Player 1"
        self.score = 0
        self.secondes = 0
        self.case_valeur_joueur.clear()
        self._rafraichir_vue()
        self._timer.start(1000)
        self.sauvegarde_auto()

    def timer_actif(self):
        return self._timer.isActive()

    def _tick(self):
        self.secondes += 1
        m, s = divmod(self.secondes, 60)
        if self.fenetre_jeu:
            self.fenetre_jeu.maj_timer(f"{m:02d}:{s:02d}")

    def sauvegarde_auto(self):
        if not self.fenetre_jeu:
            return
        cases_serialisees = {f"{x},{y}": val for (x, y), val in self.case_valeur_joueur.items()}
        data = {
            "nom_joueur": self.nom_joueur,
            "score": self.score,
            "secondes": self.secondes,
            "cases_joueur": cases_serialisees,
            "grille_path": self.chemin_json,
            "pause": not self.timer_actif(),
        }
        with open(FICHIER_SAUVEGARDE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)