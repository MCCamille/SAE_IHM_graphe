import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                              QLineEdit, QFrame, QHBoxLayout, QVBoxLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from Controleur import Controleur


class widget(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('SAE Graphes')
        self.ctrl = Controleur()

        # --- Titre ---
        titre = QLabel("Nom du jeu")
        titre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titre.setFont(QFont("Arial", 24, QFont.Weight.Bold))

        # --- Zone de jeu ---
        self.zone_jeu = QWidget()
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
        self.nom_valeur.setText(nom);   
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
        self.ctrl.reset(self.champ_nom.text()); self._fermer_menu()

    def _toggle_menu(self, checked):
        self.menu_panel.setVisible(checked)
        self.menu_btn.setText("Menu  ✕" if checked else "Menu  ☰")

    def _fermer_menu(self):
        self.menu_panel.setVisible(False)
        self.menu_btn.setChecked(False)
        self.menu_btn.setText("Menu  ☰")

    def _sep(self):
        f = QFrame(); f.setFrameShape(QFrame.Shape.HLine)
        f.setStyleSheet("color: #444;"); return f


if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = widget()
    sys.exit(app.exec())