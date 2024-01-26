import math

class Vecteur():
    def __init__(self, x, y):
        """double double double-> vecteur
        Initialisation d'un vecteur"""
        
        # Composantes du vecteur
        self.x = x
        self.y = y

        # Norme du vecteur
        self.norme = math.sqrt(self.x**2 + self.y**2 )
    
    def add(self, vecteur):
        """Vecteur vecteur -> Vecteur
        Additionne deux vecteurs"""
        return Vecteur(self.x + vecteur.x, self.y + vecteur.y)

    def soustraction(self, vecteur):
        """Vecteur vecteur -> Vecteur
        Soustrait deux vecteurs"""
        return Vecteur(self.x - vecteur.x, self.y - vecteur.y)

    def rotation(self, degre):
        """float degre -> Vecteur
        Fait une rotation vectorielle"""

        # Conversion degrés en radians
        rad = degre * (math.pi / 180)

        # Nouvelles composantes
        new_x = self.x * math.cos(rad) - self.y * math.sin(rad)
        new_y = self.x * math.sin(rad) + self.y * math.cos(rad)

        return Vecteur(new_x, new_y)
    
    def getCoor(self):
        """ -> Tuple[double, double]
        renvoie les coordonnees du vecteur sous forme de tuple
        """
        return (self.x, self.y)
    
    def produit_scalaire(self, autre_vecteur):
        """ Vecteur -> float
        """
        return self.x * autre_vecteur.x + self.y * autre_vecteur.y
        

