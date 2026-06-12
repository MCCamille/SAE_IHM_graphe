from PyQt6.QtCore import QTimer

class Controleur:
    def __init__(self):
        self._vue = None
        self.nom_joueur = "Player 1"
        self.score = 0
        self.secondes = 0
        self.case_selectionnee = None
        self.grille = None
        self._timer = QTimer()
        self._timer.timeout.connect(self._tick)
        self._timer.start(1000)

    def set_grille(self, grille):
        self.grille = grille

    def selectionner_case(self, x, y):
        if self.grille is None:
            return
        case = self.grille.get_case(y, x)
        if not case.fixe:
            self.case_selectionnee = (x, y)
        else:
            self.case_selectionnee = None
        self._vue.zone_jeu.update()

    def saisir_valeur(self, valeur):
        if self.case_selectionnee is None or self.grille is None:
            return
        x, y = self.case_selectionnee
        case = self.grille.get_case(y, x)
        if self.grille.peut_placer(case, valeur):
            self.grille.modifier_case(y, x, valeur)
            self._vue.zone_jeu.case_valeur[(x, y)] = valeur
            self._vue.zone_jeu.case_erreur = None
        else:
            self._vue.zone_jeu.case_erreur = (x, y)
        self._vue.zone_jeu.update()

    def effacer_valeur(self):
        if self.case_selectionnee is None or self.grille is None:
            return
        x, y = self.case_selectionnee
        self.grille.modifier_case(y, x, None)
        self._vue.zone_jeu.case_valeur[(x, y)] = 0
        self._vue.zone_jeu.update()

    def set_vue(self, vue):
        self._vue = vue
        self._vue.maj_nom(self.nom_joueur)
        self._vue.maj_score(self.score)
        self._vue.maj_timer("00:00")

    def appliquer_nom(self, nom):
        self.nom_joueur = nom.strip() or "Player 1"
        self._vue.maj_nom(self.nom_joueur)

    def toggle_pause(self):
        if self._timer.isActive():
            self._timer.stop()
            self._vue.maj_pause(True)
        else:
            self._timer.start(1000)
            self._vue.maj_pause(False)

    def reset(self, nom):
        self.appliquer_nom(nom)
        self.score = 0
        self.secondes = 0
        self._vue.maj_score(0)
        self._vue.maj_timer("00:00")
        if not self._timer.isActive():
            self._timer.start(1000)
            self._vue.maj_pause(False)

    def _tick(self):
        self.secondes += 1
        m, s = divmod(self.secondes, 60)
        self._vue.maj_timer(f"{m:02d}:{s:02d}")