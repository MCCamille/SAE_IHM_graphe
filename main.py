from generation import creer_grille_jeu, generer_motifs_aleatoires
from Grille import Grille

from generation import creer_grille_jeu

def main():
    print("Générateur de Néonaure")

    grille = creer_grille_jeu()

    if grille is None:
        print("Impossible de générer une grille valide.")
        return

    print("\n--- Motifs (ids) ---")
    grille.afficher_motifs()

    print("\n--- Grille de départ ---")
    grille.afficher_valeurs()

    nom_fichier = "grille_sudoku.json"
    grille.sauvegarder_json(nom_fichier)
    print(f"\nGrille sauvegardée dans : {nom_fichier}")


if __name__ == "__main__":
    main()