class Case:
    def __init__(self, ligne, colonne):
        self.ligne = ligne
        self.colonne = colonne
        self.valeur = None
        self.fixe = False
        self.id_motif = None

    #Renvoie si la case n'a pas de valeur
    def est_vide(self):
        return self.valeur is None