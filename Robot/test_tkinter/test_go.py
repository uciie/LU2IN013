from robot import *
from grille import *
from tkinter import *
from math import *
def main():

    """Création grille"""
    grille = Grille(20, 20, 1)

    """Création vecteur"""
    vecteur = Vecteur(0, 1)

    """Création canvas"""
    root=Tk()
    cnv=Canvas(root, width=20, height=20, bg="ivory")
    """Création robot"""
    robot = Robot("r", 10, 10, 1, 1 ,grille, vecteur, cnv, "red")
    robot.draw()

    """Déplacement robot"""
    robot.go(90, 5, 1)
main()