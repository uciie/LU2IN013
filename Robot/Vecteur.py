class Vecteur():
    def __init__(self, nom, xa, ya, xb, yb):
        """string nom float xa float ya float xb float yb -> vecteur
        Initialisation d'un vecteur"""
        
        # Nom du vecteur
        self.nom = nom

        # Coordonnées du premier point
        self.xa = xa
        self.ya = ya

        # Coordonées du second point
        