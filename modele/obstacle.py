from .vecteur import Vecteur

class Obstacle():
    def __init__(self, posX : float, posY :float, v1 : Vecteur, v2 : Vecteur, v3 : Vecteur, v4 : Vecteur):
        """ Initialise un obstacle

        :param posX: Coordonnée X de l'obstacle (float)
        :param posY: Coordonnée y de l'obstacle (float)
        :param v1: Vecteur directeur de l'obstacle
        :param v2: Vecteur directeur de l'obstacle
        :param v3: Vecteur directeur de l'obstacle
        :param v4: Vecteur directeur de l'obstacle
        """

        # Coordonnées du centre de l'obstacle
        self.posX = posX
        self.posY = posY

        # Vecteurs directeurs de l'obstacle
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.v4 = v4

    def getCoins(self):
        """ Renvoie les coordonnées des 4 coins de l'obstacle
        
        """
        x1, y1 = self.posX - self.v1.x / 2, self.posY - self.v2.y / 2
        x2, y2 = self.posX + self.v1.x / 2, self.posY - self.v2.y / 2
        x3, y3 = self.posX - self.v1.x / 2, self.posY + self.v2.y / 2
        x4, y4 = self.posX + self.v1.x / 2, self.posY + self.v2.y / 2

        return [x1, y1, x2, y2, x3, y3, x4, y4]
