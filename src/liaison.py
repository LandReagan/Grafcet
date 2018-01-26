import xml.etree.ElementTree as ET

from logger import logD
from grafcet_error import GrafcetError
from element import Element
from etape import Etape
from transition import Transition


class Liaison(Element):
    """ Une liaison relie une étape à une transition et elle est orientée.
        Si elle est "amont", elle part d'une ou plusieurs étapes et va vers
        une transition. S'il y a plusieurs étapes, la liaison est dite
        "synchronisée" (chaque étape doit être active pour la rendre passante).
        Si elle est "avale", elle part d'une transition et va vers plusieurs
        étapes.
        Une liaison est située sur la case de sa transition, sauf si elle
        revient plus haut dans le diagramme.
    """

    auto_numerotation = 0

    def __init__(
            self,
            etapes=None,
            transition=None,
            X=0,
            Y=0,
            amont=True,
            numero=None):
        Element.__init__(self, X, Y, 3)
        self._etapes = []
        if isinstance(etapes, Etape):
            self._etapes.append(etapes)
        elif isinstance(etapes, list):
            for etape in etapes:
                assert isinstance(etape, Etape)
            self._etapes.extend(etapes)
        self._transition = transition
        if transition is not None and X != 0 and Y != 0:
            self.X = transition.X
            self.Y = transition.Y
        self._amont = amont
        self._numero = Liaison.auto_numerotation if numero is None else numero
        Liaison.auto_numerotation += 1
        logD(str(self))

    def __str__(self):
        liste_etapes = ""
        for etape in self._etapes:
            liste_etapes += str(etape.numero) + ','
        if self._transition is None:
            numero_transition = None
        else:
            numero_transition = self._transition.numero
        return (
            "L{} X:{} Y:{} étapes:{} transition:{} amont:{}"
            .format(self.numero, self.X, self.Y, liste_etapes,
                    numero_transition, str(self.amont))
        )

    # PROPRIÉTÉS :

    @property
    def transition(self):
        return self._transition

    @property
    def etapes(self):
        return self._etapes

    @property
    def amont(self):
        return self._amont

    @property
    def synchronisee(self):
        return len(self._etapes) > 1

    @property
    def numero(self):
        return self._numero

    @property
    def variable(self):
        return '-' + ('XX' if self.numero is None else str(self.numero)) + '-'

    @property
    def franchissable(self):
        if self.amont:
            if len(self.etapes) > 0 and\
                    all(etape.active for etape in self.etapes):
                return True
        return False

    @property
    def estLiee(self):
        """ Vérifie si la liaison est connectée """
        if len(self.etapes) == 0 or self.transition is None:
            return False
        return True

    @property
    def xml(self):
        return self._xml()

    # MÉTHODES PUBLIQUES :

    def deXml(self, element_xml, elements_diagramme):
        """ Construit l'élément à partir d'un élément xml et des éléments
            du diagramme étapes et transitions.
        """
        # 1. Identification des étapes et des transitions :
        etapes = []
        transitions = []
        for element in elements_diagramme:
            if isinstance(element, Etape):
                etapes.append(element)
            if isinstance(element, Transition):
                transitions.append(element)
        # 2. Création de la Liaison
        self.X = int(element_xml.get('X'))
        self.Y = int(element_xml.get('Y'))
        if element_xml.get('numero') is not None:
            self._numero = int(element_xml.get('numero'))
        self._amont = True if element_xml.get('amont') == 'True' else False
        # Liaison aux étapes, code un peu plus complexe...
        numeros_etapes = str(element_xml.get('etapes')).split(sep=',')
        for numero in numeros_etapes:
            if numero is not '':
                try:
                    self._etapes.append(
                        next(etape for etape in etapes if
                             etape.numero == int(numero)))
                except StopIteration as error:
                    raise GrafcetError(
                        "Erreur d'intégrité XML : une liaison ({}) essaie de\
                        s'attacher à une étape ({}) qui n'existe pas !"
                        .format(self.numero, numero))
        # Liaison à la transition :
        try:
            self._transition = next(
                transition for transition in transitions if
                transition.numero == int(element_xml.get('transition')))
            if self._transition is not None and self.X == 0 and self.Y == 0:
                self.X = self._transition.X
                self.Y = self._transition.Y
        except StopIteration as error:
                raise GrafcetError(
                    "Erreur d'intégrité XML : une liaison ({}) essaie de\
                    s'attacher à une transition ({}) qui n'existe pas !"
                    .format(self.numero, int(element_xml.get('transition'))))

    # MÉTHODES PRIVÉES:

    def _xml(self):
        element_xml = ET.Element('Liaison')
        element_xml.set('X', str(self.X))
        element_xml.set('Y', str(self.Y))
        element_xml.set('numero', str(self.numero))
        element_xml.set('amont', str(self.amont))
        numero_etapes = ""
        for etape in self._etapes:
            numero_etapes += str(etape.numero) + ','
        element_xml.set('etapes', str(numero_etapes))
        element_xml.set('transition', str(self.transition.numero))
        element_xml.set('synchronisee', str(self.synchronisee))
        element_xml.tail = '\n'
        return element_xml


if __name__ == '__main__':

    etape1 = Etape(X=0, Y=0, numero=10)
    etape2 = Etape(X=0, Y=1, numero=20)
    transition1 = Transition(X=1, Y=0, numero=10)
    etape3 = Etape(X=0, Y=2, numero=30)
    liaison1 = Liaison(
        etapes=[etape1, etape2], transition=transition1, amont=True)
    liaison2 = Liaison(
        etapes=etape3, transition=transition1, amont=False)
    print(liaison1, liaison2)
