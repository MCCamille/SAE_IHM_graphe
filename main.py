from generation import Grille,creer_grille_jeu

def main():
    grille = Grille(8, 8)

    # Cette unique fonction s'occupe de TOUT créer sans aucune erreur possible
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

if __name__ == "__main__":
    main()