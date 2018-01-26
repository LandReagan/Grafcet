from xml.etree.ElementTree import parse, ParseError
from xml.parsers.expat import ErrorString
from copy import deepcopy

from logger import logI, logD
from etape import Etape
from transition import Transition
from liaison import Liaison
from grafcet_error import GrafcetError


class Diagramme:
    """ Le diagramme Grafcet est composé d'un dictionnaire d'éléments (étapes,
        transitions, liaisons), dont les clés sont leurs identifiants.
    """

    def __init__(self):
        self._elements = {}

    def __str__(self):
        retour = (
            "Diagramme.__str__ : {} éléments trouvés dans le Diagramme !\n"
            .format(len(self.elements)))
        for etape in sorted(self.etapes, key=lambda etape: etape.variable):
            retour += str(etape) + '\n'
        for transition in sorted(
                self.transitions, key=lambda trans: trans.variable):
            retour += str(transition) + '\n'
        for liaison in sorted(
                self.liaisons, key=lambda liaison: liaison.variable):
            retour += str(liaison) + '\n'
        return retour

    # PROPRIÉTÉS :

    @property
    def situation(self):
        """ Retourne les identifiants des étapes et leurs activités associés
            dans un dictionnaire.
        """
        etapes = {}
        for element in self._elements.values():
            if isinstance(element, Etape):
                etapes[str('E' + str(element.numero))] = element.active
        return etapes

    @property
    def elements(self):
        """ Retourne seulement les objets, sans leurs identifiants."""
        return self._elements.values()

    @property
    def etapes(self):
        retour = []
        for element in self.elements:
            if isinstance(element, Etape):
                retour.append(element)
        return retour

    @property
    def transitions(self):
        retour = []
        for element in self.elements:
            if isinstance(element, Transition):
                retour.append(element)
        return retour

    @property
    def liaisons(self):
        retour = []
        for element in self.elements:
            if isinstance(element, Liaison):
                retour.append(element)
        return retour

    # MÉTHODES PUBLIQUES :

    def ajouterElement(self, element):
        if isinstance(element, Etape):
            identifiant = 'E' + str(element.numero)
        elif isinstance(element, Transition):
            identifiant = 'T' + str(element.numero)
        elif isinstance(element, Liaison):
            identifiant = 'L' + str(element.numero)
        else:
            raise GrafcetError(
                "Un élément de type inconnu est passé à :\
                Diagramme.ajouterElement()")
        if identifiant not in self._elements.keys():
            self._elements[identifiant] = element
        else:
            raise GrafcetError(
                "Tentative d'ajout d'un élément muni d'un identifiant déjà\
                utilisé")

    def etapeNumero(self, numero):
        for etape in self.etapes:
            if etape.numero == numero:
                return etape
        return None

    def transitionNumero(self, numero):
        for transition in self.transitions:
            if transition.numero == numero:
                return transition
        return None

    def initialiserSituation(self):
        for etape in self.etapes:
            etape.activer() if etape.initiale else etape.desactiver()

    def calculerEvolution(self):
        """ Conforme au chapitre 4.5 de la norme """
        situation_initiale = deepcopy(self.situation)
        situation_intermediaire = deepcopy(self.situation)
        while True:
            # 1. Détermination des liaisons amonts franchissables
            liaisons_amont_franchissables = list(
                liaison for liaison in self.liaisons if liaison.franchissable)
            # 2. Détermination des transitions "validées"
            transitions_validees = list(
                liaison.transition for liaison
                in liaisons_amont_franchissables)
            # 3. Détermination des transitions franchies
            transitions_franchies = list(
                transition for transition in transitions_validees
                if transition.receptivite)
            # 4. Détermination des étapes à désactiver
            groupes_etapes_desactivees = list(
                liaison.etapes for liaison in liaisons_amont_franchissables
                if liaison.transition in transitions_franchies)
            # 5. Détermination des étapes à activer
            groupes_etapes_activees = list(
                liaison.etapes for liaison in self.liaisons
                if liaison.amont is False and
                liaison.transition in transitions_franchies)
            for etapes in groupes_etapes_desactivees:
                for etape in etapes:
                    etape.desactiver()
            for etapes in groupes_etapes_activees:
                for etape in etapes:
                    etape.activer()
            print("liaisons_amont_franchissables")
            for liaison in liaisons_amont_franchissables:
                print(liaison)
            print("transitions_validees")
            for transition in transitions_validees:
                print(transition)
            print("transitions_franchies")
            for transition in transitions_franchies:
                print(transition)
            print("groupes_etapes_desactivees")
            for etapes in groupes_etapes_desactivees:
                for etape in etapes:
                    print(etape)
            print("groupes_etapes_activees")
            for etapes in groupes_etapes_activees:
                for etape in etapes:
                    print(etape)
            print(self.situation)
            if situation_intermediaire == self.situation:  # pas d'évolution
                break  # on sort de la méthode calculerEvolution
            situation_intermediaire = deepcopy(self.situation)
            if situation_intermediaire == situation_initiale:
                raise GrafcetError("Évolution infinie du Grafcet !")

    def sauvegarderXML(self, fichier):
        """ Le fichier est écrasé """
        try:
            arbre = parse(source='../XML/diagramme_vide.xml')
            etapes = arbre.find('Etapes')
            transitions = arbre.find('Transitions')
            liaisons = arbre.find('Liaisons')
            for element in self._elements.values():
                if isinstance(element, Etape):
                    etapes.append(element.xml)
                elif isinstance(element, Transition):
                    transitions.append(element.xml)
                elif isinstance(element, Liaison):
                    liaisons.append(element.xml)
            arbre.write(
                fichier, encoding='unicode', short_empty_elements=False)
        except ParseError as e:
            raise GrafcetError('Erreur du Parser XML/nMessage : ' + e.message)

    def chargerXML(self, fichier):
        """ Vide le dictionnaire elements et le remplit avec les données du
            fichier XML """
        logI("Chargement du fichier " + str(fichier) + "...")
        self._elements.clear()
        try:
            arbre = parse(source=fichier)
        except FileNotFoundError as e:
            raise GrafcetError("Fichier : " + str(fichier) + " introuvable !")
        except ParseError as e:
            raise GrafcetError(
                "Erreur lors du chargement du fichier XML : " + fichier +
                "\nMessage du module XML : " + ErrorString(e.code))
        # TODO : vérifier intégrité du fichier xml
        etapes = arbre.find('Etapes')
        transitions = arbre.find('Transitions')
        liaisons = arbre.find('Liaisons')

        for etape_xml in etapes.findall('Etape'):
            etape = Etape()
            etape.deXml(etape_xml)
            logD(etape)
            self._elements['E' + str(etape.numero)] = etape

        for transition_xml in transitions.findall('Transition'):
            transition = Transition()
            transition.deXml(transition_xml)
            logD(transition)
            self._elements['T' + str(transition.numero)] = transition

        for liaison_xml in liaisons.findall('Liaison'):
            liaison = Liaison()
            liaison.deXml(liaison_xml, self._elements.values())
            logD(liaison)
            self._elements['L' + str(liaison.numero)] = liaison

        logI(str(len(self._elements)) + " éléments trouvés !")


if __name__ == '__main__':
    diag = Diagramme()
    etape1 = Etape(numero=10)
    transition1 = Transition(X=0, Y=1, numero=11)
    liaison1 = Liaison(etape1, transition1)
    diag.ajouterElement(etape1)
    diag.ajouterElement(transition1)
    diag.ajouterElement(liaison1)
    print(diag.situation)

    diag.chargerXML('../XML/diagramme.xml')
    print(diag.situation)

    print("Vérification des méthodes d'accès :")
    for etape in diag.etapes:
        print(etape)
    for transition in diag.transitions:
        print(transition)
    for liaison in diag.liaisons:
        print(liaison)
    print("Initialisation du diagramme :")
    diag.initialiserSituation()
    print(diag.situation)
    diag.calculerEvolution()
    diag.transitionNumero(11)._condition = "True"
    diag.calculerEvolution()

    diag.sauvegarderXML('../XML/test.xml')

