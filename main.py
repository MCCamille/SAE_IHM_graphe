import os

from generation import Grille,creer_grille_jeu

def main():
    grille = Grille(8, 8)

    grille.generer_jeu_parfait()

    print("--- VERIFICATION DE LA SOLUTION COMPLETE ---")
    grille.afficher_valeurs()
    print("--------------------------------------------")

    # On creuse la grille pour le joueur
    creer_grille_jeu(grille)

    print("\n--- GRILLE FINALE DU JOUEUR ---")
    grille.afficher_valeurs()

    print("\n--- CONFIGURATION DES MOTIFS ---")
    grille.afficher_motifs()
    
    grille.sauvegarder_json("grille_sudoku.json")
    
    # Ceci va t'afficher EXACTEMENT où le fichier est enregistré sur ton ordinateur
    print(f"Le fichier JSON a été mis à jour ")

if __name__ == "__main__":
    main()