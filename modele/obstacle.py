from .vecteur import Vecteur

class Obstacle():
    def __init__(self, posX : float, posY :float, length : float, width : float, v1 : Vecteur, v2 : Vecteur, v3 : Vecteur, v4 : Vecteur):
        """ Initialise un obstacle

        :param posX: Coordonnée X de l'obstacle (float)
        :param posY: Coordonnée y de l'obstacle (float)
        :param length: Longueur de l'obstacle (float)
        :param width: Largeur de l'obstacle (float)
        """

        # Coordonnées du centre de l'obstacle
        self.posX = posX
        self.posY = posY

        # Dimensions du robot
        self.length = length
        self.width = width

        # Vecteurs directeurs de l'obstacle
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.v4 = v4
