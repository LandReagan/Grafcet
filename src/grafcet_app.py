from kivy.app import App

from logger import logI
from gui import GUI
from controleur import Controleur
from diagramme import Diagramme


class GrafcetApp(App):
    """ Classe principale de l'application. Elle lance le modèle de données
        (classe Diagramme), la GUI (dépendante de kivy - www.kivy.org),
        et le contrôleur (classe Controleur).
    """

    diagramme = Diagramme()
    controleur = Controleur(diagramme)
    gui = GUI(controleur)

    def build(self):
        logI('Chargement de Kivy...')
        return self.gui


if __name__ == '__main__':
    logI("Démarrage de l'application !")
    GrafcetApp().run()
