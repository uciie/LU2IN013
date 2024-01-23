from Robot import *
from Grille import *



def main():
    g = Grille(5,5)
    r = Robot("Dexter", 2, 2, 1, 1, g)
    
    print("Etat initial")
    g.addRobot(r)
    g.affiche()

    print("Etat final")
    r.go(2)
    g.affiche()

main()