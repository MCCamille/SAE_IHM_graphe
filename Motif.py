class Motif:
    def __init__(self, motif_id, cases: list):
        self.motif_id = motif_id
        self.cases = cases
        self.taille = len(cases)