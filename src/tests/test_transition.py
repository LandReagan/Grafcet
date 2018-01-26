from transition import Transition


class TestTransition:

    transition_vide = Transition()

    def testTransitionVide(self):
        t = self.transition_vide
        assert t.X == 0
        assert t.Y == 0
        assert t.numero is None
        assert t.variable == '(None)'
        assert t.condition == 'False'
        assert t.receptivite is False
