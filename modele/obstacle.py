class Obstacle():
    def __init__(self, posX : float, posY :float, length : float, width : float):
        """ Initialise un obstacle

        :param posX: Coordonnée X de l'obstacle (float)
        :param posY: Coordonnée y de l'obstacle (float)
        :param length: Longueur de l'obstacle (float)
        :param width: Largeur de l'obstacle (float)
        """

        self.posX = posX
        self.posY = posY
        self.length = length
        self.width = width
