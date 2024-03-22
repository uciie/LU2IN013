import math


class Vecteur:
    def __init__(self, x: float, y: float) -> None:
        """ Initialise un vecteur.

        :param x: Coordonnée x du vecteur.
        :param y: Coordonnée y du vecteur.
        :returns: Retourne le vecteur (x, y) de longueur norme.
        """
        # Composantes du vecteur
        self._x = x
        self._y = y

        # Norme du vecteur
        self._norme: float = math.sqrt(self._x ** 2 + self._y ** 2)

    @property
    def x(self) -> float:
        """ Propriété pour l'attribut x
        :returns: La position en x du vecteur
        """
        return self._x

    @property
    def y(self) -> float:
        """ Propriété pour l'attribut y
        :returns: La position en y du vecteur
        """
        return self._y

    @property
    def norme(self) -> float:
        """ Propriété pour l'attribut norme
        :returns: La norme du vecteur
        """
        return self._norme

    @property
    def angle(self) -> float:
        """ Renvoie l'angle du vecteur en radians.

        :returns: Angle en radians du vecteur.
        """
        return math.atan2(self._y, self._x)

    def add(self, vecteur: 'Vecteur') -> 'Vecteur':
        """ Additionne deux vecteurs.

        :param vecteur: Vecteur (x, y) à ajouter.
        :returns: Renvoie la somme entre le vecteur self et le vecteur en paramètre.
        """
        return Vecteur(self.x + vecteur.x, self.y + vecteur.y)

    def soustraction(self, vecteur: 'Vecteur') -> 'Vecteur':
        """ Soustrait deux vecteurs.

        :param vecteur: Vecteur (x, y) à soustraire.
        :returns: Renvoie la différence entre le vecteur self et le vecteur en paramètre.
        """
        return Vecteur(self.x - vecteur.x, self.y - vecteur.y)

    def multiplication(self, n: float) -> 'Vecteur':
        """ Multiplier vecteur par n

        :param n: La valeur de multiplication
        :returns: Renvoie la différence entre le vecteur self et le vecteur en paramètre.
        """
        return Vecteur(n * self.x, n * self.y)

    def rotation(self, degre: float) -> 'Vecteur':
        """ Effectue une rotation vectorielle.

        :param degre: Angle de rotation en degrés.
        :returns: Nouveau vecteur résultant de la rotation du vecteur self selon l'angle spécifié.
        """
        # Conversion degrés en radians
<<<<<<< HEAD
        rad: float = -degre * (math.pi / 180)
        
        # Nouvelles composantes
        new_x: int = self.x * math.cos(rad) - self.y * math.sin(rad)
        new_y: int = self.x * math.sin(rad) + self.y * math.cos(rad)
        
=======
        rad = -degre * (math.pi / 180)

        # Nouvelles composantes
        new_x = self.x * math.cos(rad) - self.y * math.sin(rad)
        new_y = self.x * math.sin(rad) + self.y * math.cos(rad)

>>>>>>> test_robot_irl
        return Vecteur(new_x, new_y)

    def equals(self, autre_vecteur: 'Vecteur') -> bool:
        """ Vérifie l'égalité entre deux vecteurs.

        :param autre_vecteur: Vecteur avec lequel vérifier l'égalité.
        :returns: True si les deux vecteurs sont égaux, False sinon.
        """
        return autre_vecteur.x == self._x and autre_vecteur.y == self._y
