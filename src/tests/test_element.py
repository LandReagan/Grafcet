from element import Element


class TestElement:

    element_vide = Element()
    un_element_construit = Element(1, 2, 3)

    def testElementVide(self):
        e = self.element_vide
        assert e.X == 0
        assert e.Y == 0
        assert e.index == 0

    def testElementConstruit(self):
        e = self.un_element_construit
        assert e.X == 1
        assert e.Y == 2
        assert e.index == 3
