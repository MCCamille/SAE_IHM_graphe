import sys
from PyQt6.QtWidgets import (QApplication, QHBoxLayout, QWidget, 
                              QVBoxLayout, QPushButton, QLabel)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class widget(QWidget):
    
    def __init__(self):
        super().__init__()

        # configuration de la fenêtre
        self.setWindowTitle('SAE Graphes')

        # --- Widgets ---
        self.titre = QLabel("Nom du jeu")
        self.titre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titre.setFont(QFont("Arial", 24, QFont.Weight.Bold))

        self.stats = QLabel("Stats ?")
        self.stats.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Zone de jeu (espace réservé)
        self.zone_jeu = QWidget()
        self.zone_jeu.setStyleSheet("background-color: lightblue;")
        self.zone_jeu.setFixedSize(750, 700)  

        # Boutons droite
        self.menu = QPushButton("Menu  ☰")
        self.pause_btn = QPushButton("Pause  ⏸")
        self.quitter_top = QPushButton("Quitter  ✕")

        # --- Layouts ---
        self.vlayout_main = QVBoxLayout()
        self.hlayout_centre = QHBoxLayout()
        self.vlayout_gauche = QVBoxLayout()
        self.vlayout_droite = QVBoxLayout()
        self.vlayout_jeu = QVBoxLayout()  

        self.setLayout(self.vlayout_main)

        # --- Colonne gauche ---
        self.vlayout_gauche.addWidget(self.titre)
        self.vlayout_gauche.addWidget(self.stats)
        self.vlayout_gauche.addStretch()

        # --- Zone de jeu centrée verticalement ---
        self.vlayout_jeu.addStretch()
        self.vlayout_jeu.addWidget(self.zone_jeu, alignment=Qt.AlignmentFlag.AlignCenter)
        self.vlayout_jeu.addStretch()

        # --- Colonne droite ---
        # --- Colonne droite ---
        self.vlayout_droite.addStretch(3)        # ← pousse les boutons vers le bas
        self.vlayout_droite.addWidget(self.menu)
        self.vlayout_droite.addSpacing(10)       # ← espace entre Menu et Pause
        self.vlayout_droite.addWidget(self.pause_btn)
        self.vlayout_droite.addSpacing(10)       # ← espace entre Pause et Quitter
        self.vlayout_droite.addWidget(self.quitter_top)
        self.vlayout_droite.addStretch(3)        # ← petit stretch en bas

        # --- Assemblage ligne centrale ---
        self.hlayout_centre.addLayout(self.vlayout_gauche, stretch=1)
        self.hlayout_centre.addLayout(self.vlayout_jeu, stretch=3)   
        self.hlayout_centre.addLayout(self.vlayout_droite, stretch=1)
        self.hlayout_centre.setContentsMargins(10, 15, 10, 10)

        # --- Layout principal ---
        self.vlayout_main.addLayout(self.hlayout_centre)
        self.showMaximized()


# --- main -----------------------------------------------------------------
if __name__ == "__main__":
    print(' --- main --- ')
    app = QApplication(sys.argv)
    fenetre = widget()
    sys.exit(app.exec())