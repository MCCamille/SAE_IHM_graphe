class Motif:
    def __init__(self, motif_id, cases: list):
        self.motif_id = motif_id
        self.cases = cases
        self.taille = len(cases)

    def valeurs_presentes(self):
        return [c.valeur for c in self.cases if c.valeur is not None]

    def est_complet(self):
        return all(not c.est_vide() for c in self.cases)

    def est_valide(self):
        valeurs = self.valeurs_presentes()
        if len(valeurs) != len(set(valeurs)):
            return False
        if self.est_complet():
            return sorted(valeurs) == list(range(1, self.taille + 1))
        return True