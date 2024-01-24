from math import *
class Vecteur():
    def __init__(self, nom, xa, ya, xb, yb):
        """string nom float xa float ya float xb float yb -> vecteur
        Initialisation d'un vecteur"""
        
        # Nom du vecteur
        self.nom = nom
        
        #Composantes du vecteur
        self.composantes = ((xb-xa), (yb-ya))

        #Norme du vecteur
        self.norme = math.sqrt((xb-xa)**2+(yb-ya)**2)
    
    def add(self, vecteur):
        """Vecteur vecteur -> Vecteur
        Additionne deux vecteurs"""

        a, b = self.composantes
        c, d = vecteur.composantes
        self.composantes = ((a+c), (b+d))