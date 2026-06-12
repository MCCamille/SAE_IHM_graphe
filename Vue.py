import json
import os
from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton,
                              QLineEdit, QFrame, QHBoxLayout, QVBoxLayout)
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QFont, QPainter, QColor, QPen

from Controleur import Controleur

# Couleur de fond pour les cases sans motif
COULEUR_NEUTRE = QColor("#e8f0f5")

# Couleurs pastels par motif (background des cases)
COULEURS_MOTIF = [
    QColor("#aed6f1"), QColor("#f1948a"), QColor("#f9c784"),
    QColor("#a9dfbf"), QColor("#d2b4de"), QColor("#a2d9ce"),
    QColor("#f9e4b7"), QColor("#b2bec3"), QColor("#d5b8a8"),
    QColor("#f5b7b1"), QColor("#aab7d4"), QColor("#a8d5cc"),
    QColor("#e4f2a1"), QColor("#fce5a3"), QColor("#c5e1a5"),
]


class GrilleWidget(QWidget):
    """Affiche une grille 8×8 lue depuis un fichier JSON."""

    TAILLE_GRILLE = 8

    def __init__(self, chemin_json: str, parent=None):
        super().__init__(parent)
        self.motifs: dict = {}
        self.case_motif: dict = {}
        self.case_valeur: dict = {}
        self._charger(chemin_json)

    def _charger(self, chemin: str):
        with open(chemin, encoding="utf-8") as f:
            data = json.load(f)
        for idx, (nom, cases) in enumerate(data.items()):
            self.motifs[nom] = cases
            for triplet in cases:
                x, y, val = triplet
                self.case_motif[(x, y)] = idx
                self.case_valeur[(x, y)] = val

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()
        n = self.TAILLE_GRILLE
        marge = 20
        taille_case = min((w - 2 * marge) // n, (h - 2 * marge) // n)
        grille_px = taille_case * n
        ox = (w - grille_px) // 2
        oy = (h - grille_px) // 2

        # Fond des cases coloré par motif (pastel)
        for y in range(n):
            for x in range(n):
                idx = self.case_motif.get((x, y), -1)
                couleur = COULEURS_MOTIF[idx % len(COULEURS_MOTIF)] if idx >= 0 else COULEUR_NEUTRE
                rect = QRect(ox + x * taille_case, oy + y * taille_case,
                             taille_case, taille_case)
                painter.fillRect(rect, couleur)

        # Grille fine
        painter.setPen(QPen(QColor("#000000"), 1))
        for i in range(n + 1):
            painter.drawLine(ox + i * taille_case, oy, ox + i * taille_case, oy + grille_px)
            painter.drawLine(ox, oy + i * taille_case, ox + grille_px, oy + i * taille_case)

        # Valeurs spéciales
        font = QFont("Arial", max(8, taille_case // 4), QFont.Weight.Bold)
        painter.setFont(font)
        for (x, y), val in self.case_valeur.items():
            if val != 0:
                rect = QRect(ox + x * taille_case, oy + y * taille_case,
                             taille_case, taille_case)
                painter.setPen(QColor("#222222"))
                painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, str(val))

        painter.end()


class Vue(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('SAE Graphes')
        self.ctrl = Controleur()

        # --- Titre ---
        titre = QLabel("Nom du jeu")
        titre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titre.setFont(QFont("Arial", 24, QFont.Weight.Bold))

        # --- Zone de jeu ---
        chemin_json = os.path.join(os.path.dirname(os.path.abspath(__file__)), "grille_sudoku.json")
        self.zone_jeu = GrilleWidget(chemin_json)
        self.zone_jeu.setStyleSheet("background-color: lightblue;")
        self.zone_jeu.setFixedSize(750, 700)

        # --- Stats ---
        self.nom_valeur   = QLabel("Player 1")
        self.score_valeur = QLabel("0")
        self.timer_valeur = QLabel("00:00")

        self.nom_valeur.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        self.score_valeur.setStyleSheet("color: #f0c040; font-size: 14px; font-weight: bold;")
        self.timer_valeur.setStyleSheet("color: #40c0f0; font-size: 14px; font-weight: bold;")

        stats_frame = QFrame()
        stats_frame.setFixedWidth(220)
        stats_frame.setStyleSheet("QFrame { border: 2px solid #555; border-radius: 8px; background-color: #1e1e1e; }")

        sl = QVBoxLayout(stats_frame)
        sl.setContentsMargins(10, 10, 10, 10)
        sl.setSpacing(6)
        for label_txt, valeur in [("Joueur", self.nom_valeur),
                                   ("Score",  self.score_valeur),
                                   ("Temps",  self.timer_valeur)]:
            lbl = QLabel(label_txt)
            lbl.setStyleSheet("color: #aaaaaa; font-size: 11px;")
            sl.addWidget(lbl)
            sl.addWidget(valeur)
            sl.addWidget(self._sep())

        # --- Boutons droite ---
        btn_style = """QPushButton { color: white; background: #2a2a2a; border: 1px solid #555;
                        border-radius: 4px; padding: 6px 8px; }
                       QPushButton:hover { background: #3a3a3a; }"""

        self.menu_btn  = QPushButton("Menu  ☰")
        self.pause_btn = QPushButton("Pause  ⏸")
        quitter_btn    = QPushButton("Quitter  ✕")

        for b in (self.menu_btn, self.pause_btn, quitter_btn):
            b.setStyleSheet(btn_style)

        self.menu_btn.setCheckable(True)
        self.menu_btn.clicked.connect(self._toggle_menu)
        self.pause_btn.clicked.connect(self.ctrl.toggle_pause)
        quitter_btn.clicked.connect(self.close)

        # --- Panneau menu ---
        self.menu_panel = QFrame()
        self.menu_panel.setFixedWidth(220)
        self.menu_panel.setVisible(False)
        self.menu_panel.setStyleSheet("QFrame { border: 1px solid #555; border-radius: 6px; background: #1a1a1a; }")

        self.champ_nom = QLineEdit("Player 1")
        self.champ_nom.setStyleSheet("""QLineEdit { background: #2e2e2e; color: white;
            border: 1px solid #555; border-radius: 4px; padding: 5px; font-size: 13px; }""")
        self.champ_nom.returnPressed.connect(self._on_appliquer)

        btn_appliquer = QPushButton("Appliquer")
        btn_appliquer.setStyleSheet("""QPushButton { background: #2e4a2e; color: #80e080;
            border: 1px solid #4a8a4a; border-radius: 4px; padding: 5px; }""")
        btn_appliquer.clicked.connect(self._on_appliquer)

        btn_reset = QPushButton("Recommencer  ↺")
        btn_reset.setStyleSheet("""QPushButton { color: #f0c040; background: #2a2510;
            border: 1px solid #f0c040; border-radius: 4px; padding: 5px; }""")
        btn_reset.clicked.connect(self._on_reset)

        pl = QVBoxLayout(self.menu_panel)
        pl.setContentsMargins(12, 12, 12, 12)
        pl.setSpacing(8)
        header = QLabel("⚙  Paramètres")
        header.setStyleSheet("color: #aaaaaa; font-size: 12px; font-weight: bold; border: none;")
        nom_lbl = QLabel("Nom du joueur")
        nom_lbl.setStyleSheet("color: #aaaaaa; font-size: 11px; border: none;")
        pl.addWidget(header)
        pl.addWidget(self._sep())
        pl.addWidget(nom_lbl)
        pl.addWidget(self.champ_nom)
        pl.addWidget(btn_appliquer)
        pl.addWidget(self._sep())
        pl.addWidget(btn_reset)

        # --- Assemblage ---
        col_gauche = QVBoxLayout()
        col_gauche.addWidget(titre)
        col_gauche.addStretch(2)
        col_gauche.addWidget(stats_frame, alignment=Qt.AlignmentFlag.AlignHCenter)
        col_gauche.addStretch(3)

        col_jeu = QVBoxLayout()
        col_jeu.addStretch()
        col_jeu.addWidget(self.zone_jeu, alignment=Qt.AlignmentFlag.AlignCenter)
        col_jeu.addStretch()

        col_droite = QVBoxLayout()
        col_droite.addStretch(2)
        col_droite.addWidget(self.menu_btn)
        col_droite.addWidget(self.menu_panel)
        col_droite.addSpacing(10)
        col_droite.addWidget(self.pause_btn)
        col_droite.addSpacing(10)
        col_droite.addWidget(quitter_btn)
        col_droite.addStretch(3)

        centre = QHBoxLayout()
        centre.addLayout(col_gauche, stretch=1)
        centre.addLayout(col_jeu, stretch=3)
        centre.addLayout(col_droite, stretch=1)
        centre.setContentsMargins(10, 15, 10, 10)

        main = QVBoxLayout(self)
        main.addLayout(centre)

        self.ctrl.set_vue(self)
        self.showMaximized()

    # --- Méthodes appelées par le Contrôleur ---
    def maj_nom(self, nom):
        self.nom_valeur.setText(nom)
        self.champ_nom.setText(nom)

    def maj_score(self, score):
        self.score_valeur.setText(str(score))

    def maj_timer(self, texte):
        self.timer_valeur.setText(texte)

    def maj_pause(self, pause):
        self.pause_btn.setText("Reprendre  ▶" if pause else "Pause  ⏸")

    # --- Slots UI ---
    def _on_appliquer(self):
        self.ctrl.appliquer_nom(self.champ_nom.text())

    def _on_reset(self):
        self.ctrl.reset(self.champ_nom.text())
        self._fermer_menu()

    def _toggle_menu(self, checked):
        self.menu_panel.setVisible(checked)
        self.menu_btn.setText("Menu  ✕" if checked else "Menu  ☰")

    def _fermer_menu(self):
        self.menu_panel.setVisible(False)
        self.menu_btn.setChecked(False)
        self.menu_btn.setText("Menu  ☰")

    def _sep(self):
        f = QFrame()
        f.setFrameShape(QFrame.Shape.HLine)
        f.setStyleSheet("color: #444;")
        return f

