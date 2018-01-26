from etape import Etape


class TestEtape:

    etape_vide = Etape()

    def testEtapeVide(self):
        e = self.etape_vide
        assert e.X == 0
        assert e.Y == 0
        assert e.numero is None
        assert e.initiale is False
        assert e.active is False
        assert isinstance(e.actions, list)
        assert len(e.actions) == 0

        assert e.estFonctionnelle is False
        e.changerNumero(10)
        assert e.estFonctionnelle is True

    def testEtapeActivation(self):
        e = self.etape_vide
        e.activer()
        assert e.active
        e.desactiver()
        assert not e.active

    """ TODO :
    - Ajouter les tests pour les actions
    - Ajouter les tests XML, donc développer une fixture
    """
