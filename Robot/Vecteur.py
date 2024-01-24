from math import *
class Vecteur():
    def __init__(self, composantes):
        """tuple composantes -> vecteur
        Initialisation d'un vecteur"""
        
        # Nom du vecteur
        self.nom = nom
        
        #Composantes du vecteur
        self.composantes = composantes

        #Norme du vecteur
        self.norme = math.sqrt((xb-xa)**2+(yb-ya)**2)
    
    def add(self, vecteur):
        """Vecteur vecteur -> Vecteur
        Additionne deux vecteurs"""

        a, b = self.composantes
        c, d = vecteur.composantes
        return Vecteur((a+c), (b+d))
    
    def soustraction(self, vecteur):
        """Vecteur vecteur -> Vecteur
        Soustrait deux vecteurs"""

        a, b = self.composantes
        c, d = vecteur.composantes
        return Vecteur((a-c), (b-d))

    def rotation(self, degre):
        """float degre -> Vecteur
        Fait une rotation vectorielle"""

        #Conversion degrés en radians
        rad = degre * (math.pi / 180)

        #Calcul du sinus
        sin = math.sin(rad)

        #Calcul du cosinus
        cos = math.cos(rad)

        #Nouvelles composantes
        new_x = x * cos - y * sin
        new_y = x * sin + y * cos



        return Vecteur(new_x, new_y)