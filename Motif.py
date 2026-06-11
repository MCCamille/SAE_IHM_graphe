class Motif:
    def __init__(self, motif_id, cases: list):
        self.motif_id = motif_id
        self.cases = cases

    def taille(self):
        return len(self.cases)

    def valeurs_presentes(self):
        resultat = []
        for c in self.cases:
            if c.valeur is not None:
                resultat.append(c.valeur)
        return resultat

    def est_complet(self):
        for c in self.cases:
            if c.est_vide():
                return False
        return True

    def est_valide(self):
        valeurs = self.valeurs_presentes()
        if len(valeurs) != len(set(valeurs)):
            return False
        if self.est_complet():
            return sorted(valeurs) == list(range(1, self.taille + 1))
        return True