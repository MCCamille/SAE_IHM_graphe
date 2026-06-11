from PyQt6.QtCore import QTimer


class Controleur:

    def __init__(self):
        self._vue = None
        self.nom_joueur = "Player 1"
        self.score = 0
        self.secondes = 0

        self._timer = QTimer()
        self._timer.timeout.connect(self._tick)
        self._timer.start(1000)

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