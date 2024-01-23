from Robot import *
from Grille import *



def main():
    g = Grille(20,20)
    r = Robot("Dexter", 1, 1, 1, 1, g)
    
    g.affiche()

main()