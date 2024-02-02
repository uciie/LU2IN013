import math

class Vecteur():
    def __init__(self, x, y):
        """Initialisation d'un vecteur
        :param x: coordonnee x du vecteur
        :param y: coordonnee y du vecteur
        :returns: retourne le vecteur (x,y)de longueur norme """
        
        # Composantes du vecteur
        self.x = x
        self.y = y

        # Norme du vecteur
        self.norme = math.sqrt(self.x**2 + self.y**2 )
    
    def add(self, vecteur):
        """Additionne deux vecteurs
        :param vecteur: on donne un vecteur (x,y) a la methode
        :returns: elle renvoie l'addition entre le vecteur self et le vecteur en parametre"""
        
        return Vecteur(self.x + vecteur.x, self.y + vecteur.y)

    def soustraction(self, vecteur):
        """Soustrait deux vecteurs
        :param vecteur: on donne un vecteur (x,y) a la methode
        :returns: elle renvoie la soustraction entre le vecteur self et le vecteur en parametre"""
        
        return Vecteur(self.x - vecteur.x, self.y - vecteur.y)

    def rotation(self, degre):
        """Effectue une rotation vectorielle
        :param degre: Angle de rotation en degrés
        :returns: Nouveau vecteur résultant de la rotation du vecteur self selon l'angle spécifié
        """
        
        # Conversion degrés en radians
        rad = degre * (math.pi / 180)

        # Nouvelles composantes
        new_x = self.x * math.cos(rad) - self.y * math.sin(rad)
        new_y = self.x * math.sin(rad) + self.y * math.cos(rad)
        
        return Vecteur(new_x, new_y)
    
    def getCoor(self):
        """Renvoie les coordonnées du vecteur sous forme de tuple
        :returns: Tuple (double, double) représentant les coordonnées (x, y) du vecteur
        """
        return (self.x, self.y)
    
    def produit_scalaire(self, autre_vecteur):
        """Calcule le produit scalaire entre deux vecteurs
        :param autre_vecteur: Vecteur avec lequel calculer le produit scalaire
        :returns: Valeur du produit scalaire entre le vecteur self et le vecteur en paramètre
        """
        return self.x * autre_vecteur.x + self.y * autre_vecteur.y
    
    def equals(self, autre_vecteur):
        """Vérifie l'égalité entre deux vecteurs
        :param autre_vecteur: Vecteur avec lequel vérifier l'égalité
        :returns: True si les deux vecteurs sont égaux, False sinon
        """
        return autre_vecteur.x == self.x and autre_vecteur.y == self.y
    


