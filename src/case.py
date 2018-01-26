import kivy
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, BooleanProperty, ListProperty

from grafcet_error import GrafcetError
import dessins
from etape import Etape
from transition import Transition
from liaison import Liaison

kivy.require('1.10.0')


class Case(Widget):
    """ Une case se définit par ses coordonnées dans le diagramme, qu'on
        considère comme un tableau.
        ATTENTION : les coordonnées des cases commencent à 0,0 en haut à
        gauche. Par contre, kivy impose les coordonnées graphiques en bas
        à gauche.
        Cette classe contient en plus des instructions graphiques selon
        l'élément éventuellement contenu (étape, transition, ...).
    """

    X = NumericProperty(0)
    Y = NumericProperty(0)
    largeur = NumericProperty(0)
    grille_visible = BooleanProperty(True)
    elements = ListProperty(None)

    def __init__(self, X, Y, largeur, elements=None, **kwargs):
        Widget.__init__(self, **kwargs)
        self.X = X
        self.Y = Y
        self.largeur = largeur
        self.width = largeur
        self.height = largeur
        self.elements = []
        if elements is not None:
            self.elements.append(elements)
        self.reDessiner()

    def __str__(self):
        return str(
            "Case en X:{} Y:{} pos:{},{} largeur:{} centre:{},{} elements:"
            .format(
                self.X, self.Y, self.x, self.y, self.width,
                self.center_x, self.center_y, self.elements)
        )

    # PROPRIÉTÉS :

    def on_pos(self, *args):
        self.reDessiner()

    def on_elements(self, *args):
        self.reDessiner()

    @property
    def index(self):
        """ Méthode spéciale utilisée pour trier une liste de cases par index
            graphique. L'index 0 est le dernier à être dessiné, c'est donc la
            liaison, puis 1 pour transition et 2 pour étape, 3 pour vide.
        """
        if len(self.elements) == 0:
            return 0
        return max(element.index for element in self.elements)

    # MÉTHODES PUBLIQUES :

    def reDessiner(self):
        self.canvas.clear()
        self.canvas.add(dessins.dessinerFond(self))
        if self.grille_visible:
            self.canvas.add(dessins.dessinerGrille(self))
        if len(self.elements) > 0:
            self.dessinerElement()

    def dessinerElement(self):
        """ Calcul des coordonnées bas-gauche du carré inscrit dans le widget
            puis dessin de l'élément pour chaque élément.
        """
        for element in self.elements:
            if isinstance(element, Etape):
                self.canvas.add(dessins.dessinerEtape(self, element))
            elif isinstance(element, Transition):
                self.canvas.add(dessins.dessinerTransition(self, element))
            elif isinstance(element, Liaison):
                self.canvas.add(dessins.dessinerLiaison(self, element))
            else:
                raise GrafcetError(
                    "Un élément inconnu a été passé à la méthode : \
                     case.Case.dessinerElement()" + str(element))


if __name__ == "__main__":
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.button import Button
    from kivy.clock import Clock

    class TestApp(App):

        def __init__(self, **kwargs):
            App.__init__(self, **kwargs)
            self.etape = Etape(numero=10, active=True, initiale=True)
            self.transition = Transition(numero=10)

        def build(self):
            self.case = Case(0, 0, 100, self.etape)
            boxlayout = BoxLayout(orientation='vertical')
            bouton_tests = Button(text='Tests !')
            bouton_tests.bind(on_press=self.lancerTests)
            boxlayout.add_widget(bouton_tests)
            boxlayout.add_widget(self.case)
            return boxlayout

        step = 1

        def lancerTests(self, dt):
            print('Tests !')
            if self.step == 1:
                self.case.element = self.etape
                self.etape.desactiver()
            elif self.step == 2:
                self.case.element = self.etape
                self.etape.activer()
            elif self.step == 3:
                self.case.element = self.transition
            else:
                self.step = 0
            self.step += 1
            self.case.reDessiner()
            Clock.schedule_once(self.lancerTests, 1)

    TestApp().run()
