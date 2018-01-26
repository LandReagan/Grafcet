from kivy.uix.widget import Widget
from kivy.properties import ListProperty, NumericProperty
from kivy.lang.builder import Builder

from logger import logD
from case import Case

Builder.load_file("zone_dessin.kv")


class ZoneDessin(Widget):
    """ Ce widget sert à accueillir les cases et à les positionner. On lui
        envoie la liste des éléments du diagramme, il calcule les cases
        requises et les construit.
    """

    largeur = NumericProperty(80)
    elements = ListProperty(None)
    cases = ListProperty(None)

    # Coordonnées cases :
    max_X = NumericProperty(2)
    min_X = NumericProperty(0)
    max_Y = NumericProperty(2)
    min_Y = NumericProperty(0)
    # Coordonnées graphiques :
    max_x = NumericProperty(0)
    min_x = NumericProperty(0)
    max_y = NumericProperty(0)
    min_y = NumericProperty(0)

    # Callbacks des propriétés Kivy :

    def on_size(self, *args):
        self.reDessiner()

    # Méthodes publiques :

    def caseXY(self, X, Y):
        """ Retourne la case en X,Y, si elle existe. None sinon."""
        for case in self.cases:
            if case.X == X and case.Y == Y:
                return case

    def reDessiner(self):
        logD("ZoneDessin.reDessiner() !")
        # 1. On retire les widgets
        self.clear_widgets()
        # 2. On recalcule les dimensions et les cases
        self.calculerDimensions()
        self.calculerCases()
        # 3. On trie les cases par index puis on les ajoute à la ZoneDessin.
        list.sort(self.cases, key=lambda case: case.index)
        for case in self.cases:
            self.add_widget(case)
        print(len(self.elements))
        for element in sorted(self.elements, key=lambda element: element.numero):
            print(element)

    def calculerDimensions(self):
        if len(self.elements) == 0:
            return
        # 1. Calcul des dimensions de la grille.
        self.min_X = min(element.X for element in self.elements) - 1
        self.max_X = max(element.X for element in self.elements) + 1
        self.min_Y = min(element.Y for element in self.elements) - 1
        self.max_Y = max(element.Y for element in self.elements) + 1
        # 2. Décalage des coordonnées des éléments pour que la grille
        # commence en 0, 0 et mise à jour des max_X et max_Y :
        for element in self.elements:
            element.X -= self.min_X
            element.Y -= self.min_Y
        self.max_X -= self.min_X
        self.max_Y -= self.min_Y
        self.min_X = 0
        self.min_Y = 0
        # 3. Calcul des coordonnées min et max contenant les cases
        self.min_x = self.center_x - (self.max_X + 1) * self.largeur / 2
        self.max_x = self.min_x + (self.max_X + 1) * self.largeur
        self.min_y = self.center_y - (self.max_Y + 1) * self.largeur / 2
        self.max_y = self.min_y + (self.max_Y + 1) * self.largeur

    def calculerCases(self):
        # 1. Création des cases, munies de leur éventuel élément
        self.cases.clear()
        for Y in range(self.max_Y + 1):
            for X in range(self.max_X + 1):
                case = Case(X=X, Y=Y, largeur=self.largeur)
                case.x = self.min_x + X * self.largeur
                case.y = self.max_y - (Y + 1) * self.largeur
                self.cases.append(case)
        for element in self.elements:
            self.caseXY(element.X, element.Y).elements.append(element)

    def __str__(self):
        message = (
            """État de ZoneDessin :\nDimensions :
            min_X {}, min_Y {}, max_X {}, max_Y {}
            min_x {}, min_y {}, max_x {}, max_y {}
Nombre d'éléments : {}, nombre de cases : {}, nombre de widgets : {}
Cases:\n"""
            .format(self.min_X, self.min_Y, self.max_X, self.max_Y,
                    self.min_x, self.min_y, self.max_x, self.max_y,
                    len(self.elements), len(self.cases), len(self.children)))
        for case in self.cases:
            message += str(case) + '\n'
        for element in self.elements:
            message += str(element) + '\n'
        return message


if __name__ == "__main__":

    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout
    from diagramme import Diagramme

    class TestApp(App):
        def build(self):
            diag = Diagramme()
            diag.chargerXML("test.xml")
            print(diag)
            zone_dessin = ZoneDessin()
            zone_dessin.elements.extend(diag.elements)
            boxlayout = BoxLayout()
            boxlayout.add_widget(zone_dessin)
            return boxlayout

    TestApp().run()
