import xml.etree.ElementTree as ET

from action import Action
from element import Element


class Etape(Element):
    """ Une étape se définit selon la norme par :
        - Un numéro, qui forme sa "variable", s'il est associé à la lettre X
        exemple : 'X11' est la variable de l'étape 11. Elle est vraie si
        l'étape est active, fausse sinon.
        - Une activité : l'étape est active ou inactive.
        - Sa nature, initiale ou non
        - Les actions qui lui sont associées. Ses actions peuvent être une
        description ou une variable (interne, ou externe, c.a.d une sortie).
        Voir la classe 'Action'
    """

    def __init__(
            self,
            X=0,
            Y=0,
            numero=None,
            initiale=False,
            active=False,
            actions=None):
        Element.__init__(self, X, Y, 1)
        self._numero = numero
        self._initiale = initiale
        self._active = active
        self._actions = list()
        self._actions.append(actions) if actions is not None else None

    def __str__(self):
        return ("E{} variable:{} X:{} Y:{} initiale:{} active:{} actions:{}"
                .format(self.numero, self.variable, self.X, self.Y,
                        self._initiale, self._active, self._actions))

# PROPRIÉTÉS :
    @property
    def numero(self):
        return self._numero

    @property
    def initiale(self):
        return self._initiale

    @property
    def active(self):
        return self._active

    @property
    def actions(self):
        """ Retourne la liste des actions
            TODO : Revoir en fonction de la forme des actions
        """
        return self._actions

    @property
    def variable(self):
        return "X" + str(self.numero)

    @property
    def xml(self):
        """ retourne l'étape sous forme d'un élément xml """
        return self._xml()

    @property
    def estFonctionnelle(self):
        if self.numero is None:
            return False
        return True

# MÉTHODES PUBLIQUES :
    def activer(self):
        self._active = True

    def desactiver(self):
        self._active = False

    def changerNumero(self, numero):
        if isinstance(numero, int):
            self._numero = numero

    def ajouterAction(self, action):
        if isinstance(action, Action):
            self._actions.append(action)

    def deXml(self, element_xml):
        """ Construit l'élément à partir d'un élément xml.
            ATTENTION : le cast empêche toute erreur xml d'être détectée !
            TODO : implémenter les actions.
        """
        self.X = int(element_xml.get('X'))
        self.Y = int(element_xml.get('Y'))
        self._numero = int(element_xml.get('numero'))
        self._active = True if element_xml.get('active') == 'True' else False
        self._initiale = \
            True if element_xml.get('initiale') == 'True' else False

# MÉTHODES PRIVÉES :
    def _xml(self):
        element = ET.Element('Etape')
        element.set('X', str(self.X))
        element.set('Y', str(self.Y))
        element.set('numero', str(self.numero))
        element.set('initiale', str(self.initiale))
        element.set('active', str(self.active))
        element.tail = '\n'
        return element
