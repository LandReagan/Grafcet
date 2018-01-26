from kivy.graphics import Color, Rectangle, Line, Ellipse
from kivy.graphics.instructions import InstructionGroup
from kivy.uix.label import Label

# Liste des couleurs :
blanc = Color(1, 1, 1, 1)
gris = Color(0.6, 0.6, 0.6, 1)
gris_clair = Color(0.4, 0.4, 0.4, 1)
rouge = Color(1, 0, 0, 1)
vert = Color(0, 1, 0, 1)
bleu = Color(0, 0, 1, 1)
noir = Color(0, 0, 0, 1)


# Définition des dessins :
def dessinerFond(case):
    dessin_fond = InstructionGroup()
    dessin_fond.add(blanc)
    dessin_fond.add(
        Rectangle(pos=case.pos, size=case.size))
    label = Label(
        text=str(case.X) + ',' + str(case.Y),
        font_size=int(case.largeur / 5),
        color=gris_clair.rgba)
    label.texture_update()
    texture = label.texture
    dessin_fond.add(Rectangle(
        texture=texture,
        pos=[case.x, case.y],
        size=label.texture.size))
    return dessin_fond


def dessinerGrille(case):
    dessin_grille = InstructionGroup()
    dessin_grille.add(gris)
    dessin_grille.add(
        Line(rectangle=[case.x, case.y, case.largeur, case.largeur]))
    return dessin_grille


def dessinerEtape(case, etape):
    dessin_etape = InstructionGroup()
    # 1. Calcul des coordonnées bas-gauche du carré extérieur : (cas où le
    # widget n est pas carré)
    carre_inscrit = [case.x, case.y]
    largeur = min(case.width, case.height)
    if case.width > largeur:
        carre_inscrit[0] += (case.width - largeur) / 2
    elif case.height > largeur:
        carre_inscrit[1] += (case.height - largeur) / 2
    carre_inscrit_x = carre_inscrit[0]
    carre_inscrit_y = carre_inscrit[1]
    # 2. Rectangle extérieur de l'étape (toujours dessiné)
    dessin_etape.add(bleu)
    dessin_etape.add(Line(
        rectangle=[
            carre_inscrit_x + largeur * 0.2,
            carre_inscrit_y + largeur * 0.2,
            largeur * 0.6,
            largeur * 0.6]))
    # 3. Numéro d'étape (toujours dessiné, "XX" si Etape.numero vaut None)
    # TODO : Adapter la taille de la texture à la position
    numero = 'XX' if etape.numero is None else etape.numero
    label = Label(
        text=str(numero),
        font_size=int(largeur / 5),
        color=[0, 0, 0, 1])
    label.texture_update()
    texture = label.texture
    largeur_numero = texture.width
    dessin_etape.add(Rectangle(
        texture=texture,
        pos=[case.center_x - largeur_numero / 2, case.y + case.largeur * 0.5],
        size=label.texture.size))
    # 4. Activité
    if etape.active:
        dessin_etape.add(Ellipse(
            pos=[case.x + largeur * 0.45, case.y + largeur * 0.35],
            size=[largeur * 0.1, largeur * 0.1]))

    return dessin_etape


def dessinerTransition(case, transition):
    dessin_transition = InstructionGroup()
    largeur = min(case.width, case.height)
    dessin_transition.add(bleu)
    # 1. Barre verticale (toujours affichée)
    dessin_transition.add(Line(
        points=[case.x + case.width / 2, case.y + case.height * 0.3,
                case.x + case.width / 2, case.y + case.height * 0.7]))
    # 2. Barre horizontale (toujours affichée)
    dessin_transition.add(Line(
        points=[case.x + largeur * 0.4, case.y + case.height * 0.5,
                case.x + largeur * 0.6, case.y + case.height * 0.5]))
    numero = '(XX)' if transition.variable is None else transition.variable
    label = Label(
        text=str(numero),
        font_size=int(largeur / 5),
        color=[0, 0, 0, 1])
    label.texture_update()
    texture = label.texture
    largeur_numero = texture.width
    hauteur_numero = texture.height
    dessin_transition.add(Rectangle(
        texture=texture,
        pos=[
            case.center_x - case.largeur * 0.2 - largeur_numero,
            case.y + case.largeur * 0.5 - hauteur_numero / 2],
        size=label.texture.size))
    label = Label(
        text=str(transition.condition),
        font_size=int(largeur / 5),
        color=[0, 0, 0, 1])
    label.texture_update()
    texture = label.texture
    largeur_numero = texture.width
    hauteur_numero = texture.height
    dessin_transition.add(Rectangle(
        texture=texture,
        pos=[
            case.center_x + case.largeur * 0.2,
            case.y + case.largeur * 0.5 - hauteur_numero / 2],
        size=label.texture.size))
    return dessin_transition


def dessinerLiaison(case, liaison):
    """ Toute la collection de cases et passée
    """
    dessin_liaison = InstructionGroup()
    # 1. Récupération des éléments et de leurs coordonnées en local :
    etapes = liaison.etapes
    transition = liaison.transition
    largeur = case.largeur
    dessin_liaison.add(bleu)
    # 2. limites x du (des) traits horizontal et y
    min_X = min(etape.X for etape in etapes)
    min_X = min(min_X, transition.X, liaison.X)
    min_x = (min_X - transition.X) * largeur + case.center_x
    max_X = max(etape.X for etape in etapes)
    max_X = max(max_X, transition.X, liaison.X)
    max_x = (max_X - transition.X) * largeur + case.center_x
    y_haut_trans = case.y + largeur * 0.7
    y_bas_trans = case.y + largeur * 0.3

    if liaison.amont:
        # 1. Traits liés à l'étape
        print(liaison, min_x, y_haut_trans, max_x, y_haut_trans)
        dessin_liaison.add(Line(
            points=[min_x, y_haut_trans, max_x, y_haut_trans]))
    else:
        dessin_liaison.add(Line(
            points=[min_x, y_bas_trans, max_x, y_bas_trans]))

    return dessin_liaison
