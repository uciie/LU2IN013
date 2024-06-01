import math
import os

def project(axes: list[float], coins: list[tuple[float, float]]) -> list[float]:
    """ Projection des coins de l'obstacle sur un axe

    :param axes: Les axes de la projection
    :param coins: Les coordonnées des coins de l'obstacle
    :returns: La plus petite et la plus grande valeur de projection
    """
    min_p = max_p = axes[0] * coins[0][0] + axes[1] * coins[0][1]
    for coin_x, coin_y in coins:
        projection = axes[0] * coin_x + axes[1] * coin_y
        if projection < min_p:
            min_p = projection
        elif projection > max_p:
            max_p = projection
    return [min_p, max_p]


def distance(point1: tuple[float, float], point2: tuple[float, float]) -> float:
    """Calcul de la distance euclidienne entre deux points."""
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def point_le_plus_loin(points: list[tuple[float, float]], x_ref: float, y_ref: float) -> tuple[float, float]:
    """Trouver le point le plus loin d'un point de référence."""
    plus_loin = points[0]
    distance_min = distance(points[0], (x_ref, y_ref))

    for point in points[1:]:
        dist = distance(point, (x_ref, y_ref))
        if dist > distance_min:
            distance_min = dist
            plus_loin = point

    return plus_loin

    
def check_directory():
    """Vérifie si le dossier 'enregistrement_image' existe, sinon le crée"""
    directory = "enregistrement_image"
    if not os.path.exists(directory):
        #creer le dossier d'enregistrement pour stocker les images
        os.makedirs(directory)

class Vecteur:
    """Classe vecteur """

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
        self._norme: float = distance((self._x, self._y), (0, 0))

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
        rad = -degre * (math.pi / 180)

        # Nouvelles composantes
        new_x = self.x * math.cos(rad) - self.y * math.sin(rad)
        new_y = self.x * math.sin(rad) + self.y * math.cos(rad)

        return Vecteur(new_x, new_y)

    def equals(self, autre_vecteur: 'Vecteur') -> bool:
        """ Vérifie l'égalité entre deux vecteurs.

        :param autre_vecteur: Vecteur avec lequel vérifier l'égalité.
        :returns: True si les deux vecteurs sont égaux, False sinon.
        """
        return autre_vecteur.x == self._x and autre_vecteur.y == self._y
