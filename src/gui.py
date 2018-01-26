from logger import logD

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.properties import (
    BooleanProperty, NumericProperty, ObjectProperty, StringProperty)
from kivy.clock import Clock
from kivy.lang.builder import Builder

from etape import Etape
from case import Case

Builder.load_file('gui.kv')


class ZoneDessin(Widget):
    """ La zone de dessin reçoit le diagramme Grafcet. Elle contient un
        certain nombre de cases carrées.
    """
    largeur_case = NumericProperty(100)
    colonnes = NumericProperty(0)
    lignes = NumericProperty(0)
    largeur_zone = NumericProperty(0)
    hauteur_zone = NumericProperty(0)

    grille_visible = BooleanProperty(False)

    def __init__(self, **kwargs):
        logD("Création de la zone de dessin !")
        Widget.__init__(self, **kwargs)
        self.cases = []
        self.reDessiner()

    def reDessiner(self):
        self.calculerCases()
        self.dessinerCases()

    def calculerCases(self):
        self.cases.clear()
        decalage_x, decalage_y = self.calculerDecalage()
        for c in range(self.colonnes):
            for l in range(self.lignes):
                self.cases.append(
                    Case(
                        Y=c,
                        X=l,
                        self.hauteur_zone))

    def identifierCase(self, x, y):
        for case in self.cases:
            if case.x < x and case.y < y and\
                    x < case.x + case.largeur and y < case.y + case.largeur:
                return case

    def caseXY(self, X, Y):
        for case in self.cases:
            if case.X == X and case.Y == Y:
                return case
        else:
            print("Case introuvable à la position " + str(X) + ',' + str(Y))

    def dessinerCases(self):
        self.canvas.clear()
        for case in self.cases:
            self.canvas.add(case)

    def calculerDecalage(self):
        decalage_x = (self.size[0] - self.largeur_zone) / 2
        decalage_y = (self.size[1] - self.hauteur_zone) / 2
        return decalage_x, decalage_y

    def on_grille_visible(self, *args):
        if self.grille_visible:
            for case in self.cases:
                case.dessinerGrille()
        else:
            for case in self.cases:
                case.effacerGrille()

    def on_touch_down(self, touch):
        case = self.identifierCase(touch.x, touch.y)
        if case is None:
            return super(ZoneDessin, self).on_touch_down(touch)
        else:
            print("touch de la case {},{}".format(case.X, case.Y))
            return True

    # DEBUG
    def on_largeur_zone(self, *args):
        print("largeur_zone : " + str(self.largeur_zone))


class ZoneControle(BoxLayout):
    """ La zone de contrôle gère les événements de type boutons et autres,
        permettant l'utilisation de l'application.
    """

    controleur = None

    zone_dessin = ObjectProperty(None)

    text_edition = StringProperty('Édition')

    def modeEdition(self):
        pass

    def modeSimulation(self):
        pass

    def modeMarche(self):
        pass

    def grilleOnOff(self):
        if self.zone_dessin.grille_visible is False:
            self.zone_dessin.grille_visible = True
        else:
            self.zone_dessin.grille_visible = False

    def ajouterColonne(self):
        self.zone_dessin.colonnes += 1

    def ajouterLigne(self):
        self.zone_dessin.lignes += 1

    def lancerTests(self):
        logD('Lancement des tests !')
        self.controleur.ajouterEvenement('TEST')


class GUI(BoxLayout):
    """ La GUI contient la zone de dessin ainsi que la zone de contrôle.
        Elle gère les événements natifs de kivy pour générer les événements
        internes de l'application.
    """

    zone_dessin = ObjectProperty(None)
    zone_controle = ObjectProperty(None)
    elements = ObjectProperty(None)

    def __init__(self, controleur, *args):
        BoxLayout.__init__(self, *args)
        logD("Lancement de la GUI !")
        self.controleur = controleur
        self.zone_controle.controleur = controleur
        self.on_elements()

    def lancerControleur(self, periode):
        Clock.schedule_interval(self.miseAJour, 1 / self.controleur.periode)

    def on_elements(self, *args):
        if self.elements is None:
            self.zone_dessin.colonnes = 3
            self.zone_dessin.lignes = 3
        for element in self.elements:
            # 1. Agrandissement de la grille si requis :
            X = element.X
            Y = element.Y
            if self.zone_dessin.colonnes <= X:
                self.zone_dessin.colonnes = X + 1
            if self.zone_dessin.lignes <= Y:
                self.zone_dessin.lignes = Y + 1


if __name__ == "__main__":
    from kivy.app import App

    class AppTest(App):
        def build(self):
            return GUI(None)

    AppTest().run()
