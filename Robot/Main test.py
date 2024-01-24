from Robot import *
from Grille import *
from Obstacle import *


def main():
    g = Grille(5,5)
    r = Robot("Dexter", 2, 2, 1, 1, g)
    o = Obstacle(2,1,0,0,g)
    o.addObstacle()
    
    try:
        print("Etat initial")
        g.addRobot(r)
        g.affiche()

        print("Etat final")
        r.go(10)
        g.affiche() 
    except IndexError as e :
        pass
    print("On enlève l'obstacle")
    o.removeObstacle()
    g.affiche()
    
main()
