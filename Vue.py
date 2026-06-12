import json
import os
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QLineEdit, QFrame, QDialog,
    QHBoxLayout, QVBoxLayout, QGridLayout, QApplication
)
from PyQt6.QtCore import Qt, QRect 
from PyQt6.QtGui import QFont, QPainter, QColor, QPen, QBrush, QLinearGradient, QPixmap, QMovie

COULEUR_NEUTRE = QColor("#20252b")
COULEUR_SELECTION = QColor("#ffffff")

COULEURS_MOTIF = [
    QColor("#aed6f1"), QColor("#f1948a"), QColor("#f9c784"),
    QColor("#a9dfbf"), QColor("#d2b4de"), QColor("#a2d9ce"),
    QColor("#f9e4b7"), QColor("#b2bec3"), QColor("#d5b8a8"),
    QColor("#f5b7b1"), QColor("#aab7d4"), QColor("#a8d5cc"),
    QColor("#e4f2a1"), QColor("#fce5a3"), QColor("#c5e1a5"),
]

BTN_STYLE = """
QPushButton {
    color: #f2f2f2;
    background: #23242a;
    border: 1px solid #2f3138;
    border-radius: 12px;
    padding: 8px;
}
QPushButton:hover {
    background: #2b2c33;
}
"""

class GrilleWidget(QWidget):
    TAILLE_GRILLE = 8

    def __init__(self, chemin_json: str, ctrl, parent=None):
        super().__init__(parent)
        self.ctrl = ctrl
        self.chemin_json = chemin_json

        self.motifs = {}
        self.case_motif = {}
        self.case_valeur_fixe = {}
        self.case_valeur_joueur = {}
        self.case_selectionnee = None
        self.cases_erreurs = []

        self._marge = 20
        self._taille_case = 0
        self._ox = 0
        self._oy = 0

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.charger_structure_grille(chemin_json)

    def charger_structure_grille(self, chemin: str):
        self.motifs.clear()
        self.case_motif.clear()
        self.case_valeur_fixe.clear()
        self.case_selectionnee = None
        self.cases_erreurs.clear()

        with open(chemin, encoding="utf-8") as f:
            data = json.load(f)

        for idx, (nom, cases) in enumerate(data.items()):
            self.motifs[nom] = cases
            for triplet in cases:
                x, y, val = triplet
                self.case_motif[(x, y)] = idx
                self.case_valeur_fixe[(x, y)] = val
        self.update()

    def maj_valeurs_joueur(self, dict_valeurs):
        self.case_valeur_joueur = dict_valeurs.copy()
        self.update()

    def highlight_erreurs(self, liste_erreurs):
        self.cases_erreurs = liste_erreurs
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()
        n = self.TAILLE_GRILLE
        marge = self._marge
        taille_case = min((w - 2 * marge) // n, (h - 2 * marge) // n)
        grille_px = taille_case * n
        ox = (w - grille_px) // 2
        oy = (h - grille_px) // 2

        self._taille_case = taille_case
        self._ox = ox
        self._oy = oy

        for y in range(n):
            for x in range(n):
                idx = self.case_motif.get((x, y), -1)
                couleur = COULEURS_MOTIF[idx % len(COULEURS_MOTIF)] if idx >= 0 else COULEUR_NEUTRE
                rect = QRect(ox + x * taille_case, oy + y * taille_case, taille_case, taille_case)
                painter.fillRect(rect, couleur)

        painter.setPen(QPen(QColor("#808080"), 1))
        for i in range(n + 1):
            painter.drawLine(ox + i * taille_case, oy, ox + i * taille_case, oy + grille_px)
            painter.drawLine(ox, oy + i * taille_case, ox + grille_px, oy + i * taille_case)

        if self.case_selectionnee is not None:
            sx, sy = self.case_selectionnee
            rect = QRect(ox + sx * taille_case, oy + sy * taille_case, taille_case, taille_case)
            painter.setPen(QPen(COULEUR_SELECTION, 3))
            painter.drawRect(rect)

        font_fixe = QFont("Arial", max(10, taille_case // 4), QFont.Weight.Bold)
        font_joueur = QFont("Arial", max(10, taille_case // 4), QFont.Weight.Normal)

        for (x, y), val in self.case_valeur_fixe.items():
            if val != 0:
                rect = QRect(ox + x * taille_case, oy + y * taille_case, taille_case, taille_case)
                painter.setFont(font_fixe)
                painter.setPen(QColor("#000000"))
                painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, str(val))

        for (x, y), val in self.case_valeur_joueur.items():
            rect = QRect(ox + x * taille_case, oy + y * taille_case, taille_case, taille_case)
            painter.setFont(font_joueur)
            
            if (x, y) in self.cases_erreurs:
                painter.setPen(QColor("#cc0000"))
            else:
                painter.setPen(QColor("#000000"))
                
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, str(val))

        painter.end()

    def mousePressEvent(self, event):
        x_pix = event.position().x()
        y_pix = event.position().y()

        gx = int((x_pix - self._ox) // self._taille_case) if self._taille_case else -1
        gy = int((y_pix - self._oy) // self._taille_case) if self._taille_case else -1

        if 0 <= gx < self.TAILLE_GRILLE and 0 <= gy < self.TAILLE_GRILLE:
            self.case_selectionnee = (gx, gy)
            self.setFocus()
        else:
            self.case_selectionnee = None
            
        self.cases_erreurs.clear()
        self.update()

    def keyPressEvent(self, event):
        if self.case_selectionnee is None:
            return

        x, y = self.case_selectionnee
        if (x, y) in self.case_valeur_fixe and self.case_valeur_fixe[(x, y)] != 0:
            return

        self.cases_erreurs.clear()

        texte = event.text()
        if texte in {"1", "2", "3", "4", "5"}:
            self.ctrl.modifier_valeur_case(x, y, int(texte))
        elif event.key() in (Qt.Key.Key_Backspace, Qt.Key.Key_Delete, Qt.Key.Key_0):
            self.ctrl.modifier_valeur_case(x, y, None)

    def transmettre_bouton_num(self, valeur):
        if self.case_selectionnee is not None:
            x, y = self.case_selectionnee
            if (x, y) in self.case_valeur_fixe and self.case_valeur_fixe[(x, y)] != 0:
                return
            self.cases_erreurs.clear()
            self.ctrl.modifier_valeur_case(x, y, valeur)


class EcranAccueil(QWidget):
    def __init__(self, ctrl):
        super().__init__()
        self.ctrl = ctrl

        self.setWindowTitle("Néaunore - Accueil")
        self.resize(600, 500)
        self.bg_image = QPixmap("chat.png") 

        titre = QLabel("Néaunore")
        titre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titre.setFont(QFont("Impact", 42)) 
        titre.setStyleSheet("color: #f5f5f5; background: transparent; letter-spacing: 2px;")
        
        btn_charger = QPushButton("Continuer")
        btn_nouvelle = QPushButton("Nouvelle partie")
        btn_quitter = QPushButton("Quitter")

        for btn in (btn_charger, btn_nouvelle, btn_quitter):
            btn.setMinimumHeight(52)
            btn.setFixedWidth(280)
            btn.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #23242a;
                    color: #f5f5f5;
                    border: 1px solid #2f3138;
                    border-radius: 12px;
                    padding: 10px 16px;
                }
                QPushButton:hover {
                    background-color: #2b2c33;
                }
                QPushButton:disabled {
                    background-color: #1c2128;
                    color: #6f7a88;
                    border: 1px solid #2b313b;
                }
            """)

        btn_charger.clicked.connect(self.ctrl.charger_derniere_partie)
        btn_nouvelle.clicked.connect(self.ctrl.nouvelle_partie)
        btn_quitter.clicked.connect(QApplication.instance().quit)

        if not os.path.exists("save_partie.json"):
            btn_charger.setEnabled(False)

        layout_carte = QVBoxLayout()
        layout_carte.setContentsMargins(0, 0, 0, 0)
        layout_carte.setSpacing(18)
        layout_carte.addStretch()
        layout_carte.addWidget(titre, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_carte.addSpacing(20)
        layout_carte.addWidget(btn_charger, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_carte.addWidget(btn_nouvelle, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_carte.addWidget(btn_quitter, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_carte.addStretch()

        self.setLayout(layout_carte)

    def paintEvent(self, event):
        painter = QPainter(self)
        w, h = self.width(), self.height()
        painter.fillRect(0, 0, w, h, QColor("#1a1b1f"))

        if not self.bg_image.isNull():
            scaled_w = w
            scaled_h = int(self.bg_image.height() * (w / self.bg_image.width()))
            pix_scaled = self.bg_image.scaled(scaled_w, scaled_h, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
            
            y_pos = h - scaled_h
            painter.drawPixmap(0, y_pos, pix_scaled)

            gradient = QLinearGradient(0, y_pos, 0, h)
            gradient.setColorAt(0.0, QColor("#1a1b1f"))       
            gradient.setColorAt(0.7, QColor(26, 27, 31, 100))  
            gradient.setColorAt(1.0, QColor(26, 27, 31, 0))    
            
            painter.fillRect(0, y_pos, scaled_w, scaled_h, QBrush(gradient))


class FenetreJeu(QWidget):
    def __init__(self, chemin_json, ctrl):
        super().__init__()
        self.ctrl = ctrl
        self.chemin_json = chemin_json

        self.setWindowTitle("Néaunore")
        self.setStyleSheet("background-color: #1a1b1f;")

        self.titre_jeu = QLabel("Néaunore")
        self.titre_jeu.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titre_jeu.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        self.titre_jeu.setStyleSheet("color: #f5f5f5; background: transparent; padding-bottom: 10px;")

        self.nom_valeur = QLabel("Player 1")
        self.nom_valeur.setStyleSheet("color: #f5f5f5; font-size: 20px; font-weight: bold; background: transparent;")
        
        self.timer_valeur = QLabel("00:00")
        self.timer_valeur.setStyleSheet("color: #f5f5f5; font-size: 20px; font-weight: bold; background: transparent;")

        self.score_valeur = QLabel("Score : 0")
        self.score_valeur.setStyleSheet("color: #ffcc66; font-size: 20px; font-weight: bold; background: transparent;")

        layout_haut_grille = QHBoxLayout()
        layout_haut_grille.addWidget(self.nom_valeur, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        layout_haut_grille.addWidget(self.timer_valeur, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        layout_haut_grille.addWidget(self.score_valeur, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.zone_jeu = GrilleWidget(self.chemin_json, self.ctrl)
        self.zone_jeu.setStyleSheet("""
            background-color: #111418;
            border: 2px solid #303844;
            border-radius: 14px;
        """)
        self.zone_jeu.setFixedSize(700, 700)

        # Bouton Vérification placé en bas à droite de la grille
        self.btn_verifier = QPushButton("Vérifier")
        self.btn_verifier.setMinimumSize(140, 42)
        self.btn_verifier.setStyleSheet("""
        QPushButton {
            background-color: #233a28;
            color: #f5f5f5;
            border: 1px solid #3b6a43;
            border-radius: 10px;
            font-size: 13px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #2b4a32;
        }
        """)
        self.btn_verifier.clicked.connect(self.ctrl.verifier_grille)

        layout_bas_grille = QHBoxLayout()
        layout_bas_grille.addStretch()
        layout_bas_grille.addWidget(self.btn_verifier)

        zone_gauche_principale = QVBoxLayout()
        zone_gauche_principale.addLayout(layout_haut_grille)
        zone_gauche_principale.addWidget(self.zone_jeu)
        zone_gauche_principale.addLayout(layout_bas_grille) # Intégration en bas à droite de la grille

        self.menu_btn = QPushButton("Menu  ☰")
        self.menu_btn.setCheckable(True)
        self.menu_btn.setFixedWidth(180)
        self.menu_btn.setStyleSheet("""
        QPushButton {
            color: #f5f5f5;
            background: #23242a;
            border: 1px solid #2f3138;
            border-radius: 12px;
            padding: 10px 12px;
            font-size: 14px;
            font-weight: bold;
        }
        QPushButton:hover {
            background: #2b2c33;
        }
        """)
        self.menu_btn.clicked.connect(self._toggle_menu)

        self.menu_panel = QFrame()
        self.menu_panel.setFixedWidth(180)
        self.menu_panel.setVisible(False)
        self.menu_panel.setStyleSheet("QFrame { border: 1px solid #2f3138; border-radius: 14px; background: #23242a; }")

        self.champ_nom = QLineEdit("Player 1")
        self.champ_nom.setStyleSheet("QLineEdit { background: #111418; color: #f5f5f5; border: 1px solid #303844; border-radius: 8px; padding: 6px; font-size: 12px; }")
        self.champ_nom.returnPressed.connect(self._on_appliquer)

        btn_appliquer = QPushButton("Appliquer")
        btn_appliquer.setStyleSheet(BTN_STYLE)
        btn_appliquer.clicked.connect(self._on_appliquer)

        btn_reset = QPushButton("Recommencer  ↺")
        btn_reset.setStyleSheet(BTN_STYLE)
        btn_reset.clicked.connect(self._on_reset)

        btn_quitter = QPushButton("Quitter  ✕")
        btn_quitter.setStyleSheet(BTN_STYLE)
        btn_quitter.clicked.connect(self.close)

        pl = QVBoxLayout(self.menu_panel)
        pl.setContentsMargins(10, 10, 10, 10)
        pl.setSpacing(8)
        pl.addWidget(self.champ_nom)
        pl.addWidget(btn_appliquer)
        pl.addWidget(self._sep())
        pl.addWidget(btn_reset)
        pl.addWidget(btn_quitter)

        pav_num = self._creer_pave_numerique()

        zone_droite = QVBoxLayout()
        zone_droite.addWidget(self.menu_btn, alignment=Qt.AlignmentFlag.AlignTop)
        zone_droite.addWidget(self.menu_panel, alignment=Qt.AlignmentFlag.AlignTop)
        zone_droite.addSpacing(10)
        zone_droite.addWidget(pav_num, alignment=Qt.AlignmentFlag.AlignTop)
        zone_droite.addStretch()

        layout_jeu_et_pave = QHBoxLayout()
        layout_jeu_et_pave.addLayout(zone_gauche_principale)
        layout_jeu_et_pave.addSpacing(40)
        layout_jeu_et_pave.addLayout(zone_droite)

        layout_global = QVBoxLayout(self)
        layout_global.setContentsMargins(30, 20, 30, 30)
        layout_global.addWidget(self.titre_jeu)
        layout_global.addLayout(layout_jeu_et_pave)

        self.showMaximized()

    def _creer_pave_numerique(self):
        frame = QFrame()
        frame.setFixedWidth(180)
        frame.setStyleSheet("QFrame { background-color: #23242a; border: 1px solid #2f3138; border-radius: 14px; }")

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        grille = QGridLayout()
        grille.setSpacing(8)

        boutons = []
        for valeur in ["1", "2", "3", "4", "5"]:
            btn = QPushButton(valeur)
            btn.setMinimumSize(46, 46)
            btn.setStyleSheet("""
            QPushButton {
                background-color: #1a1b1f;
                color: #f5f5f5;
                border: 1px solid #2f3138;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2b2c33;
            }
            """)
            btn.clicked.connect(lambda _, v=int(valeur): self.zone_jeu.transmettre_bouton_num(v))
            boutons.append(btn)

        positions = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)]
        for btn, (r, c) in zip(boutons, positions):
            grille.addWidget(btn, r, c)

        btn_suppr = QPushButton("Supprimer")
        btn_suppr.setMinimumHeight(46)
        btn_suppr.setStyleSheet("""
        QPushButton {
            background-color: #3a2323;
            color: #f5f5f5;
            border: 1px solid #6a3b3b;
            border-radius: 10px;
            font-size: 13px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #4a2b2b;
        }
        """)
        btn_suppr.clicked.connect(lambda: self.zone_jeu.transmettre_bouton_num(None))

        layout.addLayout(grille)
        layout.addWidget(btn_suppr)
        return frame

    def maj_nom(self, nom):
        self.nom_valeur.setText(nom)
        self.champ_nom.setText(nom)

    def maj_score(self, score):
        self.score_valeur.setText(f"Score : {score}")

    def maj_timer(self, texte):
        self.timer_valeur.setText(texte)

    def maj_grille_joueur(self, dict_valeurs):
        self.zone_jeu.maj_valeurs_joueur(dict_valeurs)

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
        f.setStyleSheet("color: #303844;")
        return f

    def closeEvent(self, event):
        self.ctrl.sauvegarde_auto()
        super().closeEvent(event)


class PopUpVictoire(QDialog):
    """Fenêtre de félicitations stylisée incluant le chat.gif en animation continue"""
    def __init__(self, nom_joueur, score, ctrl):
        super().__init__()
        self.ctrl = ctrl
        self.setWindowTitle("Félicitations !")
        self.setFixedSize(450, 480)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setStyleSheet("background-color: #1a1b1f; border: 2px solid #303844; border-radius: 16px;")

        # CORRECTION ICI : On passe directement les flags sans le "Qt.WindowFlags" devant
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)

        lbl_titre = QLabel("VICTOIRE !")
        lbl_titre.setFont(QFont("Impact", 32))
        lbl_titre.setStyleSheet("color: #ffcc66; background: transparent; letter-spacing: 2px;")
        lbl_titre.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl_msg = QLabel(f"Bravo {nom_joueur} !\nVous avez résolu la grille.\nScore final : {score}")
        lbl_msg.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        lbl_msg.setStyleSheet("color: #f5f5f5; background: transparent;")
        lbl_msg.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.lbl_gif = QLabel()
        self.lbl_gif.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_gif.setStyleSheet("background: transparent; border: none;")
        self.lbl_gif.setFixedSize(250, 200)

        self.movie = QMovie("chat.gif")
        if self.movie.isValid():
            self.lbl_gif.setMovie(self.movie)
            self.movie.start()
        else:
            self.lbl_gif.setText("🐾 (chat.gif manquant) 🐾")
            self.lbl_gif.setStyleSheet("color: #6f7a88; font-size: 16px;")

        btn_nouvelle = QPushButton("Nouvelle grille")
        btn_nouvelle.setMinimumHeight(45)
        btn_nouvelle.setStyleSheet("""
            QPushButton {
                background-color: #233a28;
                color: #f5f5f5;
                border: 1px solid #3b6a43;
                border-radius: 12px;
                font-weight: bold;
                font-size: 13px;
                padding: 0px 20px;
            }
            QPushButton:hover { background-color: #2b4a32; }
        """)
        btn_nouvelle.clicked.connect(self.ctrl.nouvelle_partie)

        btn_quitter = QPushButton("Quitter")
        btn_quitter.setMinimumHeight(45)
        btn_quitter.setStyleSheet("""
            QPushButton {
                background-color: #3a2323;
                color: #f5f5f5;
                border: 1px solid #6a3b3b;
                border-radius: 12px;
                font-weight: bold;
                font-size: 13px;
                padding: 0px 20px;
            }
            QPushButton:hover { background-color: #4a2b2b; }
        """)
        btn_quitter.clicked.connect(QApplication.instance().quit)

        layout_boutons = QHBoxLayout()
        layout_boutons.setSpacing(20)
        layout_boutons.addWidget(btn_nouvelle)
        layout_boutons.addWidget(btn_quitter)

        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(25, 30, 25, 30)
        layout_principal.setSpacing(15)
        layout_principal.addWidget(lbl_titre)
        layout_principal.addWidget(lbl_msg)
        layout_principal.addWidget(self.lbl_gif, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_principal.addSpacing(10)
        layout_principal.addLayout(layout_boutons)