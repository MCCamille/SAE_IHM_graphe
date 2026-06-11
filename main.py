from generation import Grille,creer_grille_jeu

def main():
    # 1. Initialisation
    grille = Grille(8, 8)

    # 2. Génération de la solution secrète
    grille.remplir_chiffres_seuls()
    grille.generer_motifs_depuis_chiffres()

    # 3. Sauvegarde de la solution pour pouvoir la vérifier plus tard
    solution_complete = grille.copier_valeurs()

    # 4. Création du puzzle pour le joueur (on creuse la grille)
    creer_grille_jeu(grille)

    # 5. C'est prêt !
    print("--- GRILLE DE DÉPART DU JOUEUR ---")
    grille.afficher_valeurs() 
    # Les chiffres affichés sont ceux qui ont 'fixe = True'. Les '.' sont à remplir par le joueur.

    print("\n--- CONFIGURATION DES MOTIFS ---")
    grille.afficher_motifs()

if __name__ == "__main__":
    main()