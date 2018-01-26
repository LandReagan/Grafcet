"""
    Ce fichier configure le module standard logging de python.
    Il définit diverses fonctions pour simplifier l'écriture
    et l'utilisation de cette fonctionalité
"""

import logging

FILE_NAME = 'Grafcet.log'
LEVEL = logging.DEBUG

grafcet_log = logging.getLogger()  # renvoie le logger "racine"

handler = logging.FileHandler(FILE_NAME, mode='w')
formatter = logging.Formatter(
    fmt='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%H:%M:%S')
handler.setFormatter(formatter)
grafcet_log.addHandler(handler)
grafcet_log.setLevel(logging.DEBUG)

""" Ce script initialise le comportement du logger pour le mettre à
notre goût : les messages prendront la forme :
[niveau] HH:MM:SS - message
"""

logging.info('Démarrage du logger !')


def logD(message):
    grafcet_log.debug(message)


def logI(message):
    grafcet_log.info(message)


def logW(message):
    grafcet_log.warning(message)


def logE(message):
    grafcet_log.error(message)


def logC(message):
    grafcet_log.critical(message)


if __name__ == '__main__':
    logD('Test de logger niveau DEBUG')
    logI('Test du logger niveau INFO')
    logW('Test du logger niveau WARNING')
    logE('Test du logger niveau ERROR')
    logC('Test du logger niveau CRITICAL')
