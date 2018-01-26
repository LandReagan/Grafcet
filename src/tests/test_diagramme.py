import pytest
from pathlib import Path

from diagramme import Diagramme
from grafcet_error import GrafcetError


class TestDiagramme:

    diagramme_vide = Diagramme()
    diagramme_charge = Diagramme()
    chemin_diagramme_de_test = './XML/diagramme.xml'

    def testDiagrammeVide(self):
        d = self.diagramme_vide
        assert len(d.elements) == 0
        assert len(d.situation) == 0

    def testDiagrammeCharge(self):
        racine = Path('.')
        print([x for x in racine.iterdir()])
        d = self.diagramme_charge
        with pytest.raises(GrafcetError):
            d.chargerXML('un_fichier_qui_existe_pas.xml')
        d.chargerXML(self.chemin_diagramme_de_test)
        assert len(d.etapes) == 8, "8 étapes auraient dues être chargées"
        assert len(d.transitions) == 5, "5 transitions auraient dues être chargées"
        assert len(d.liaisons) == 11, "11 liaisons auraient dues être chargées"
