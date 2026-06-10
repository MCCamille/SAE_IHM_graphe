import random

from Case import Case
class Motif:
    def __init__(self, motif_id, cases: list):
        self.motif_id = motif_id
        self.cases = cases
        self.taille = len(cases)

    def get_cases(self):
        return self.cases
    
    def get_taille(self):
        return self.taille
    
    """Génère aléatoirement le nombre de cases que constituent un motifs (1 à 5 cases)"""
    @staticmethod
    def generer_taille_motif():
        return random.randint(1, 5)
    
    """Génère aléatoirement les cases qui constituent un motif"""
    @staticmethod
    def generer_cases_motif(taille):
        return [Case(i, fixe=False) for i in range(taille)]

    def __str__(self):  
        """"""      
        return f"Motif {self.motif_id} avec {self.taille} cases"
