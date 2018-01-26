from grafcet_error import GrafcetError


class Element:
    """ La classe Element est une interface qui permet de définir les
        coordonnées (X, Y) des éléments composant le diagramme Grafcet.
        L'index permet de définir l'élément le plus haut en cas de
        superposition.
    """

    def __init__(self, X=0, Y=0, index=0):
        self.X = X
        self.Y = Y
        self.index = index

    def case(self, cases):
        """ Retourne la case correspondante """
        for case in cases:
            if case.X == self.X and case.Y == self.Y:
                return case
        return GrafcetError(
            "Impossible de trouver la case", self.X, self.Y,
            "correspondante !")
