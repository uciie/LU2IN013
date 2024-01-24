from Robot import *
from Robot.robot_ancienne_version.Grille import *

def main():
    g = Grille(5,5)
    r = Robot("Dexter", 2, 2, 1, 1, g)
    
    try:
        print("Etat initial")
        g.addRobot(r)
        g.affiche()

        print("Etat final")
        r.go(10)
        g.affiche() 
    except IndexError as e :
        pass
    
    
main()
