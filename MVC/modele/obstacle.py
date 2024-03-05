from .vecteur import Vecteur

class Obstacle:
    def __init__(self, posX: float, posY: float, coin1: Vecteur, coin2: Vecteur, coin3: Vecteur, coin4: Vecteur, color: str):
        """ Initialise un obstacle

        :param posX: Coordonnée X de l'obstacle (float)
        :param posY: Coordonnée y de l'obstacle (float)
        :param v1: Côté haut
        :param v2: Côté bas
        :param v3: Côté gauche
        :param v4: Côté droite
        """
        # couleur de obstacle
        self._color = color 

        # Coordonnées du centre de l'obstacle
        self._posX = posX
        self._posY = posY

        # Vecteurs directeurs de l'obstacle
        self._coin1 = coin1
        self._coin2 = coin2
        self._coin3 = coin3
        self._coin4 = coin4

    @property
    def posX(self) -> float:
        """ Propriété pour l'attribut posX """
        return self._posX

    @property
    def posY(self) -> float:
        """ Propriété pour l'attribut posY """
        return self._posY

    @property
    def color(self) -> str:
        """ Propriété pour l'attribut color """
        return self._color

    @property
    def coin1(self) -> Vecteur:
        """ Propriété pour l'attribut v1 """
        return self._coin1

    @property
    def coin2(self) -> Vecteur:
        """ Propriété pour l'attribut v2 """
        return self._coin2

    @property
    def coin3(self) -> Vecteur:
        """ Propriété pour l'attribut v3 """
        return self._coin3

    @property
    def coin4(self) -> Vecteur:
        """ Propriété pour l'attribut v4 """
        return self._coin4

    @property
    def coins(self):
        """ Renvoie les coordonnées des 4 coins de l'obstacle """
        x1, y1 = self._posX + self._coin1.x / 2, self._posY - self._coin2.y / 2
        x2, y2 = self._posX + self._coin1.x / 2, self._posY + self._coin2.y / 2
        x3, y3 = self._posX - self._coin1.x / 2, self._posY + self._coin2.y / 2
        x4, y4 = self._posX - self._coin1.x / 2, self._posY - self._coin2.y / 2

        return [x1, y1, x2, y2, x3, y3, x4, y4]