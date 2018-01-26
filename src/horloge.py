from datetime import datetime

from grafcet_error import GrafcetError


def dureeMs(debut, fin):
    """ Renvoie le temps écoulé en ms entre debut et fin """
    if (isinstance(debut, datetime) and isinstance(fin, datetime)):
        duree = fin - debut
        return duree.microseconds // 1000
    else:
        raise GrafcetError(
            "La fonction Horloge.dureeMs() a été appelée avec des paramètres\
            incorrects")


class Horloge:
    """ La classe Horloge est utilisée pour la gestion du temps.
        Elle procure le temps de départ de l'application (de sa construction),

    """

    # Formats publics:
    format_jour = '%d-%m-%Y'
    format_heure = '%H:%M:%S'

    def __init__(self):
        self.demarrage_horloge = datetime.now()

    # PROPRIÉTÉS :

    @property
    def top(self):
        """ Un 'top' est un enregistrement temporel pour comparaison """
        return datetime.now()

    @property
    def heure(self):
        """ Renvoie l'heure sous forme de texte HH:MM """
        return datetime.now().strftime(self.format_heure)

    @property
    def date(self):
        """ Renvoie l'heure sous forme de texte HH:MM """
        return datetime.now().strftime(self.format_jour)


if __name__ == '__main__':
    h = Horloge()
    print(h.demarrage_horloge)
    print("Démarrage de l'horloge le ", h.date, " à ", h.heure)

    print(dureeMs(h.demarrage_horloge, h.top))
