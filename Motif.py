class Motif:
    def __init__(self, motif_id, cases: list):
        self.motif_id = motif_id
        self.cases = cases
        self.taille = len(cases)
        
    def valeurs_presentes(self) -> list:
        """Retourne la liste des valeurs placées dans le motif."""
        return [c.valeur for c in self.cases if c.valeur is not None]
 
    def est_complet(self) -> bool:
        """Retourne True si toutes les cases du motif sont remplies."""
        return all(not c.est_vide() for c in self.cases)
 
    def est_valide(self) -> bool:
        """
        Un motif de N cases doit contenir tous les chiffres de 1 à N.
        Vérifie l'absence de doublons sur les cases remplies.
        Si le motif est complet, vérifie aussi que les valeurs forment exactement {1..N}.
        """
        valeurs = self.valeurs_presentes()
        if len(valeurs) != len(set(valeurs)):
            return False
        if self.est_complet():
            return sorted(valeurs) == list(range(1, self.taille + 1))
        return True