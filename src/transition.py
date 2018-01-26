import xml.etree.ElementTree as ET

from element import Element


class Transition(Element):
    """
    """

    def __init__(
            self,
            X=0,
            Y=0,
            numero=None,
            condition='False'):
        Element.__init__(self, X, Y, 2)
        self._numero = numero
        self._condition = condition

    def __str__(self):
        return ("T{} variable:{} X:{} Y:{} condition:{}"
                .format(self.numero, self.variable, self.X, self.Y,
                        self.condition))

# PROPRIÉTÉS :
    @property
    def numero(self):
        return self._numero

    @property
    def variable(self):
        return '(' + str(self.numero) + ')'

    @property
    def condition(self):
        return self._condition

    @property
    def receptivite(self):
        return self._evaluer()

    @property
    def xml(self):
        return self._xml()

    # MÉTHODES PUBLIQUES :

    def deXml(self, element_xml):
        """ Construit l'élément à partir d'un élément xml.
            ATTENTION : le cast empêche toute erreur xml d'être détectée !
        """
        self.X = int(element_xml.get('X'))
        self.Y = int(element_xml.get('Y'))
        self._numero = int(element_xml.get('numero'))
        self._condition = str(element_xml.get('condition'))

    # MÉTHODES PRIVÉES:

    def _evaluer(self):
        return eval(self._condition)

    def _xml(self):
        element = ET.Element('Transition')
        element.set('X', str(self.X))
        element.set('Y', str(self.Y))
        element.set('numero', str(self.numero))
        element.set('condition', str(self._condition))
        element.tail = '\n'
        return element
