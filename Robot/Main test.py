from Robot import *
from Grille import *



def main():
    g = Grille(5,5)
    r = Robot("Dexter", 1, 1, 1, 1, g)
    
    g.addRobot(r)
    g.affiche()

main()