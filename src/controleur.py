from logger import logI, logW

from diagramme import Diagramme
from horloge import Horloge as H


class Controleur:
    """ Le contrôleur vérifie les entrées, calcule le diagramme puis met à jour
        les sorties à la cadence requise par la période de rafraîchissement.
    """
    periode = 1000  # période de rafraîchissement, en millisecondes.
    lag = False  # Indique si le controleur "lag"

    evenements_possibles = [
        'TEST',
    ]

    def __init__(self, diagramme=None):
        self.evenements = []
        self.diagramme = Diagramme() if diagramme is None else diagramme
        logI('Lancement du contrôleur, période de rafraîchissement: ' +
             str(self.periode) + ' millisecondes.')

    def miseAJour(self):
        # 1. Prise en compte des événements
        for e in self.evenements:
            if e == 'TEST':
                self.lancerTests()
        self.evenements.clear()
        # 2. Lecture des entrées et mise à jour des timings

        # 3. Calcul de l'évolution

        # 4. Mise à jour de la GUI par remontée du modèle

    def ajouterEvenement(self, evenement):
        if evenement in self.evenements_possibles:
            self.evenements.append(evenement)

    def lancerTests(self):
        self.diagramme.chargerXML('../XML/diagramme.xml')
        print(self.diagramme.situation)
