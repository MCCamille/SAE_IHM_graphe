import sys
from PyQt6.QtWidgets import QApplication
from Controleur import Controleur

if __name__ == "__main__":
    # 1. On initialise le framework graphique PyQt6
    app = QApplication(sys.argv)
    
    # 2. On instancie le contrôleur purement logique
    controleur = Controleur()
    
    # 3. Le contrôleur s'occupe d'ouvrir l'accueil
    controleur.demarrer_application()
    
    # 4. On écoute la fermeture globale de l'interface
    sys.exit(app.exec())