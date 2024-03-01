import math

class Vecteur():
    def __init__(self, x: int, y: int) -> None:
        """ Initialise un vecteur.

        :param x: Coordonnée x du vecteur.
        :param y: Coordonnée y du vecteur.
        :returns: Retourne le vecteur (x, y) de longueur norme.
        """
        # Composantes du vecteur
        self.x: int = x
        self.y: int = y

        # Norme du vecteur
        self.norme: float = math.sqrt(self.x**2 + self.y**2 )
    
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
        
        return Vecteur(new_x, new_y)
    
    def getAngle(self) -> float: 
        """ Renvoie l'angle du vecteur

        :returns: double représentant l'angle en radian du vecteur.
        """
        return 1/(math.cos(self.x/self.norme))
    
    def equals(self, autre_vecteur: 'Vecteur') -> bool:
        """ Vérifie l'égalité entre deux vecteurs.

        :param autre_vecteur: Vecteur avec lequel vérifier l'égalité.
        :returns: True si les deux vecteurs sont égaux, False sinon.
        """
        return autre_vecteur.x == self.x and autre_vecteur.y == self.y