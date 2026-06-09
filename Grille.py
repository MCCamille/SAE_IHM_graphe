from SAE_IHM_graphe.Case import Case
from SAE_IHM_graphe.Motif import Motif
    
class Grille:
    def __init__(self, lignes, colonnes):
        self.lignes = lignes
        self.colonnes = colonnes
        self.cases = [
            [Case(r, c) for c in range(colonnes)]
            for r in range(lignes)
        ]
        self.motifs: list[Motif] = []

    def get_case(self, ligne, colonne) -> Case:
        return self.cases[ligne][colonne]

    def get_voisins(self, cell: Case) -> list:
        """Retourne les 8 voisins (y compris diagonales)."""
        voisins = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                r, c = cell.ligne + dr, cell.colonne + dc
                if 0 <= r < self.lignes and 0 <= c < self.colonnes:
                    voisins.append(self.cases[r][c])
        return voisins

    def definir_motifs(self, motif_map: list[list[int]]):
        motifs_dict: dict[int, list[Case]] = {}
        for r in range(self.lignes):
            for c in range(self.colonnes):
                sid = motif_map[r][c]
                self.cases[r][c].motif_id = sid
                motifs_dict.setdefault(sid, []).append(self.cases[r][c])

        self.motifs = [
            Motif(sid, cases) for sid, cases in motifs_dict.items()
        ]