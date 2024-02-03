#from simulation.vecteur import *
from simulation.interface_graph import * 
from simulation.robot import *
from simulation.grille import *

import sys

def addRobot(grille, robot:Robot, dimX: int, dimY: int ):
    """ Ajouter le robot dans la grille.

    :param robot: Instance de la classe Robot à ajouter.
    :param dimX: Largeur du robot dans la grille.
    :param dimY: Hauteur du robot dans la grille.
    """
    for ligne in range(int(dimY)):
      for col in range(int(dimX)):
        grille[robot.posY+ligne][robot.posX+col] = "R" 

def inGrille(grille:Grille, posX, posY):
    """ Verifie si la position (posX, posY) est dans la grille

    :param grille: La fenetre 
    :param posX: Coordonnee en x 
    :param posY: Coordonnee en y
    :retruns bool: Renvoie true si (x,y) est dans la grille, sinon false
    """
    return 0 <= posX < grille.maxX and 0 <= posY < grille.maxY
  
def inGrille2D(grille : Grille, new_x, new_y, length, width):
    """ Si une des extremite de l'objet n'est pas dans la grille renvoyer false

    :param grille: La fenetre 
    :param new_x: Coordonnee en x 
    :param new_y: Coordonnee en y 
    :retruns bool: Renvoie true si l'objet de dim length*width est dans la grille, sinon false
    """
    #Vérifier les extremité droite et gauche de l'objet
    for ligne in range(length): 
        y= new_y - length/2+ligne
        #print(new_x-length/2,y)
        if (not inGrille(grille, new_x-length/2, y)) or (not inGrille(grille, new_x+length/2,y)) : 
            return False
    #Vérifier les extremité haut et bas de l'objet
    for col in range(width): 
        x = new_x - length/2+col
        if (not inGrille(grille, x , new_y-width/2)) or (not inGrille(grille, x, new_y+width/2)) : 
            return False
    return True

def go(grille: Grille, robot : Robot, distance: float, vitesse: int):
    """  Faire avancer le robot d'une distance avec une vitesse

    :param robot: Robot
    :param distance: La distance que le robot doit parcourir (float) 
    :param vitesse: La vitesse du robot en m/s (int)
    """
    # on modifie la vitesse du robot
    robot.vitesse = vitesse

    # compteur de distance parcourrue
    cpt_dis = 0

    #Coordonnee de vecteur de deplacement 
    dOM_x = robot.vectDir.x*vitesse*dt #/robot.grille.echelle 
    dOM_y = robot.vectDir.y*vitesse*dt #/robot.grille.echelle 
    dOM = Vecteur(dOM_x, dOM_y)
    
    #tant qu'on n'a pas fini de parcourrir tte la distance on effectue un dOM
    while cpt_dis < distance : #/robot.grille.echelle :
        
        # Si on sort de la fenetre, le robot cras
        # Il n'y a pas encore de capteur
        if not inGrille2D(grille, robot.posX, robot.posY,robot.length, robot.width):
            print(robot.name, " est a la borne : ",robot.posX, robot.posY)
            sys.exit()
        
        #Bouger le robot d'un dOM
        robot.move_dOM(dOM_x, dOM_y)

        cpt_dis += dOM.norme
    print(robot.posX,robot.posY)
    print("fin")

    
if __name__ == "__main__":
    # Dimension de la fenetre 
    largeur, hauteur = 300, 300
    bg = "white"
    interface = Interface("Simulation de déplacement du robot", largeur, hauteur, bg)

    # Position initiale du robot
    dim_robot_x, dim_robot_y = int(largeur / 10), int(hauteur / 10)

    # Assurez-vous que la grille est correctement initialisée
    grille = Grille(largeur, hauteur, 5)
    
    #Creation du robot 
    robot = Robot("R", int(largeur/2), int(hauteur/2), dim_robot_x, dim_robot_y,Vecteur(0,-1),color="red")
    print("Ini")
    print(robot.posX,robot.posY)
    distance = 10
    vitesse = 1
    go(grille, robot, distance, vitesse)


    interface.root.mainloop()