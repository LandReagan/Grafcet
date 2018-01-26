from liaison import Liaison


class TestLiaison:

    def testLiaisonVide(self):
        liaison_vide = Liaison()
        lv = liaison_vide
        assert lv.X == 0
        assert lv.Y == 0, "Y devrait être 0 pour une liaison vide !"
        assert lv.index == 3
        assert isinstance(lv.etapes, list)
        assert len(lv.etapes) == 0
        assert lv.transition is None
        assert lv.amont is True
        assert lv.numero == Liaison.auto_numerotation - 1
        assert lv.synchronisee is False
        assert lv.variable == '-' + str(lv.numero) + '-'
        assert lv.franchissable is False
        assert lv.estLiee is False
