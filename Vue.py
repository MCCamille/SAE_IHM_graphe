#Fichier de PyQt6 pour la partie graphique de l'application
import sys

from PyQt6.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox

class widget(QWidget):
    
    def __init__(self):
        super().__init__()

        # configuration de la fenêtre
        self.setWindowTitle('SAE Graphes')
        self.showMaximized()  

        # éléments widgets
        self.titre = QLabel("Titre jeu")
        self.jouer = QPushButton("Jouer")
        self.rejouer = QPushButton("Rejouer")
        self.quit = QPushButton("Quitter")
        self.pause = QPushButton("Pause")
        self.resume = QPushButton("Reprendre")



        # éléments layouts
        self.vlayout = QVBoxLayout()
        self.hlayout = QHBoxLayout()
        
        # placement widgets
        self.setLayout(self.vlayout)
        self.hlayout.addWidget(self.jouer)
        self.hlayout.addWidget(self.rejouer)
        self.hlayout.addWidget(self.pause)
        self.hlayout.addWidget(self.resume)
        self.hlayout.addWidget(self.quit)




        # placement main
        self.vlayout.addWidget(self.titre)
        self.vlayout.addStretch()
        self.vlayout.addLayout(self.hlayout)
        



        # show
        self.show()


# --- main -----------------------------------------------------------------
if __name__ == "__main__":

    print(f' --- main --- ')

    # création d'une QApplication
    app = QApplication(sys.argv)

    fenetre = widget()

    sys.exit(app.exec())