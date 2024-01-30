from robot import *

def main():

    """Création grille"""
    grille = Grille(20, 20, 1)

    """Création vecteur"""
    vecteur = Vecteur(0, 1)

    """Création canvas"""
    canvas = Canvas(10, 10, "white")
    """Création robot"""
    robot = Robot(r, 10, 10, 1, 1 ,grille, vecteur)