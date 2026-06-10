from Grille import Grille, creer_grille_jeu

def main():
    print("Générateur de Néonaure")

    taille = int(input("Taille de la grille (ex: 4, 5, 6) : "))
    nb_cases_depart = int(input("Nombre de cases visibles au départ : "))

    grille = creer_grille_jeu(
        taille=taille,
        nb_cases_depart=nb_cases_depart,
        taille_min_motif=2,
        taille_max_motif=5,
        nb_tentatives=50
    )

    if grille is None:
        print("Impossible de générer une grille valide avec ces paramètres.")
        return

    print("\n--- Motifs (ids) ---")
    grille.afficher_motifs()

    print("\n--- Grille de départ ---")
    grille.afficher_valeurs()

    print("\n--- Solution complète ---")
    for ligne in grille.solution:
        print(" ".join(str(v) for v in ligne))

    nom_fichier = "grille_sudoku.json"
    grille.sauvegarder_json(nom_fichier)
    print(f"\nGrille sauvegardée dans : {nom_fichier}")


if __name__ == "__main__":
    main()