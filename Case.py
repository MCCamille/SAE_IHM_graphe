class Case:

    def __init__(self, ligne, colonne):

        self.ligne = ligne
        self.colonne = colonne
        self.valeur = None
        self.fixe = False # True = case de départ, False = case à remplir 
        self.id_motif = None
        
    def est_vide(self) -> bool:
        """Retourne True si la case n'a pas encore de valeur."""
        return self.valeur is None