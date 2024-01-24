from Robot_v2_no_fini import *
from Grille_v2_no_fini import *
from Obstacle import *


def main():
    g = Grille(5,5)
    r = Robot("Dexter", 2, 2, 1, 1, g)
    o = Obstacle(2,1,0,0,g)

    print("Etat initial")
    g.affiche()

    for i in range(3):
        r.move_one("UP", 0)
        r.move_one("RIGHT", 0)
        print(str(i+1) + "e itération")
        g.affiche()

main()