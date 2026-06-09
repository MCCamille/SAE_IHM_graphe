class Case:

    def __init__(self, ligne, colonne, valeur, fixe):

        self.ligne = ligne
        self.colonne = colonne
        self.valeur = valeur
        self.fixe = fixe
        self.id_motif = None

        case_depart = Case(0,3,4,True)