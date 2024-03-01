import math

class Vecteur:
    def __init__(self, x: int, y: int) -> None:
        """ Initialise un vecteur.

        :param x: Coordonnée x du vecteur.
        :param y: Coordonnée y du vecteur.
        :returns: Retourne le vecteur (x, y) de longueur norme.
        """
        # Composantes du vecteur
        self._x: int = x
        self._y: int = y

        # Norme du vecteur
        self._norme: float = math.sqrt(self._x**2 + self._y**2 )
    
    @property
    def x(self) -> int:
        """ Propriété pour l'attribut x """
        return self._x
    
    @property
    def y(self) -> int:
        """ Propriété pour l'attribut y """
        return self._y

    @property
    def norme(self) -> float:
        """ Propriété pour l'attribut norme """
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
        """ Soustrait deux vecteurs.

        :param vecteur: Vecteur (x, y) à soustraire.
        :returns: Renvoie la différence entre le vecteur self et le vecteur en paramètre.
        """
        return Vecteur(n*self.x, n*self.y)
    
    def rotation(self, degre: float) -> 'Vecteur':
        """ Effectue une rotation vectorielle.

        :param degre: Angle de rotation en degrés.
        :returns: Nouveau vecteur résultant de la rotation du vecteur self selon l'angle spécifié.
        """
        # Conversion degrés en radians
        rad: float = -degre * (math.pi / 180)
        
        # Nouvelles composantes
        new_x: int = self.x * math.cos(rad) - self.y * math.sin(rad)
        new_y: int = self.x * math.sin(rad) + self.y * math.cos(rad)

        # Arrondir x et y à zéro si très proches de zéro
        if abs(new_x) < 1e-2:
            new_x = 0
        if abs(new_y) < 1e-2:
            new_y = 0
        
        return Vecteur(new_x, new_y)
    
    def equals(self, autre_vecteur: 'Vecteur') -> bool:
        """ Vérifie l'égalité entre deux vecteurs.

        :param autre_vecteur: Vecteur avec lequel vérifier l'égalité.
        :returns: True si les deux vecteurs sont égaux, False sinon.
        """
        return autre_vecteur.x == self._x and autre_vecteur.y == self._y