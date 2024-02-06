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

def tracer_parcours(interface: Interface, robot: Robot):
    """ Trace le parcours du robot

    :param interface: L'interface graphique
    :param robot: Le robot
    """
    interface.draw_parcours(robot)

def update(interface: Interface, robot: Robot):
    """ Mettre à jour l'interface graphique 

    :param interface: L'interface graphique
    :param robot: Le robot
    """
    interface.delete_draw(robot.rect_id, robot.arrow_id)
    robot.rect_id, robot.arrow_id = interface.draw_obj(robot)
    tracer_parcours(interface, robot)
    interface.root.update()

def set_vitesse(robot: Robot, vitesse, angle: int = 0):
    """ Modifier les vitesse des roues pour faire un virage d'un certain angle
    
    :param robot: Le robot 
    :param vitesse: La vitesse de pirage souhaitee
    :param angle: L'angle qu'on souhaite tourner en radian
    """
    #Mettre à jour la vitesse du robot
    robot.vitesse = min(vitesse,  robot.roue_droite.vmax_ang* robot.roue_gauche.rayon)

    #Mettre à 0 l'une des roues
    # tourner à droite
    if angle > 0 : 
        robot.roue_gauche.set_vitesse_angulaire(2.*vitesse/robot.roue_gauche.rayon)
        robot.roue_droite.set_vitesse_angulaire(0.0)
    # tourner à gauche 
    elif angle < 0 : 
        robot.roue_gauche.set_vitesse_angulaire(0.0)
        robot.roue_droite.set_vitesse_angulaire(2.*vitesse/robot.roue_droite.rayon)
    # aller tout droit
    else : 
        robot.roue_gauche.set_vitesse_angulaire(vitesse/robot.roue_gauche.rayon)
        robot.roue_droite.set_vitesse_angulaire(vitesse/robot.roue_droite.rayon)


def raytracing(capteur : Capteur, robot : Robot, grille : Grille):
    """Renvoie la distance de l'obstacle devant le capteur
    
    :param capteur : Capteur
    :param robot: Robot
    :param interface: Interface
    :returns : Distance entre le capteur et l'obstacle
    """

    #Initialisation des coordonnées
    coordonnee_x = robot.posX
    coordonnee_y = robot.posY
    nb_rayons = 0

    #Envoie un vecteur tant qu'il n'y a pas d'obstacle
    while(inGrille(grille, coordonnee_x, coordonnee_y)):
        coordonnee_x += capteur.vecteur.x
        coordonnee_y += capteur.vecteur.y
        nb_rayons+=1
    
    #Renvoie la distance
    return capteur.vecteur.norme * nb_rayons

def turn(interface: Interface, grille: Grille, robot: Robot,  vitesse: int, angle: int, dt):
    """ Tourner le robot d'un angle 

    :param interface: L'interface graphique
    :param grille: La grille
    :param robot: Le robot 
    :param vitesse: La vitesse du robot en m/s
    :param angle: L'angle qu'on souhaite tourner en degree
    """
    
    # Conversion degrés en radians
    angle_radians = math.radians(angle)
    #print("deg rad", angle_radians)

    #Modifier les vitesse angulaires des roues et robot 
    set_vitesse(robot, vitesse, angle_radians)

    #Un pas de rotation 
    dOM_theta = robot.getVitesse_angulaire()*dt
    
    # compteur d'angle parcourrue
    cpt_angle = 0

    #tant qu'on n'a pas atteint l'angle on effectue un d_theta
    while cpt_angle < angle_radians : #/robot.grille.echelle :

        # Si on sort de la fenetre, le robot crash
        # Il n'y a pas encore de capteur
        if (raytracing(robot.capteur, robot, grille) <= math.sqrt(robot.length**2 + robot.width**2)/2):
            break
        elif not inGrille2D(grille, robot.posX, robot.posY,robot.length, robot.width):
            print(robot.name, " est a la borne : ",robot.posX, robot.posY)
            sys.exit()

        #Coordonnee de vecteur de deplacement 
        dOM_x = robot.vectDir.x*robot.vitesse*dt #/robot.grille.echelle 
        dOM_y = robot.vectDir.y*robot.vitesse*dt #/robot.grille.echelle 
        
        #Bouger le robot d'un dOM avec un angle
        robot.move_dOM(dOM_x, dOM_y, dOM_theta)

        #Bouger la capteur à chaque pas
        robot.capteur.vecteur= robot.vectDir

        cpt_angle += dOM_theta
        update(interface, robot)
        print(robot.posX, robot.posY, robot.roue_droite.vitesse_angulaire,robot.roue_droite.vitesse_angulaire)

    #Remettre à jour la vitesse angulaire des roues
    set_vitesse(robot, vitesse)

def go(interface: Interface, grille: Grille, robot : Robot, distance: float, vitesse: int, dt):
    """  Faire avancer le robot d'une distance avec une vitesse

    :param interface: L'interface graphique
    :param grille: La grille
    :param robot: Robot
    :param distance: La distance que le robot doit parcourir (float) 
    :param vitesse: La vitesse du robot en m/s (int)
    """
    # Si la distance est negative on fait demi tour puis on avance
    if distance < 0:
        turn(interface, grille, robot, vitesse, 180, dt)
    # on modifie la vitesse du robot
    set_vitesse(robot, vitesse)

    # compteur de distance parcourrue
    cpt_dis = 0
    
    #Coordonnee de vecteur de deplacement 
    dOM_x = robot.vectDir.x*vitesse*dt #/robot.grille.echelle 
    dOM_y = robot.vectDir.y*vitesse*dt #/robot.grille.echelle 
    dOM = Vecteur(dOM_x, dOM_y)

    robot.capteur.vecteur= robot.vectDir
        
    #tant qu'on n'a pas fini de parcourrir tte la distance on effectue un dOM
    while cpt_dis < math.fabs(distance) : #/robot.grille.echelle :
        
        # Si on sort de la fenetre, le robot crash
        # Il n'y a pas encore de capteur
        if (raytracing(robot.capteur, robot, grille) <= math.sqrt(robot.length**2 + robot.width**2)/2):
            break
        elif not inGrille2D(grille, robot.posX, robot.posY,robot.length, robot.width):
            print(robot.name, " est a la borne : ",robot.posX, robot.posY)
            sys.exit()
        
        #Bouger le robot d'un dOM
        robot.move_dOM(dOM_x, dOM_y)

        cpt_dis += dOM.norme
        print(robot.posX, robot.posY, robot.roue_droite.vitesse_angulaire,robot.roue_droite.vitesse_angulaire)
        
        update(interface, robot)
    #print(robot.posX, robot.posY, robot.theta)

def faire_carre():
    """Le robot trace un carre distance * distance
    """
    vitesse = interface.vitesse_var.get() #recupere la valeur de la vitesse saisie
    distance = interface.distance_var.get() #recupere la valeur de la distance saisie
    angle = interface.distance_var.get() #90 recupere la valeur de l'angle de rotation saisie

    tours = 4
    for i in range(tours):
        go(interface,grille, robot, distance, vitesse, dt)
        turn(interface,grille, robot, vitesse, angle, dt)

def avance():
    """Le robot accélere avec une vitesse sur une distance sans toucher le mur 
    """
    vitesse = interface.vitesse_var.get() #recupere la valeur de la vitesse saisie
    distance = interface.distance_var.get() #recupere la valeur de la distance saisie
    go(interface,grille, robot, distance, vitesse, dt)

def accelerer_sans_colision():
    """ Le robot accélere avec une vitesse max sans toucher le mur 
    """
    distance = largeur + hauteur
    vitesse = robot.roue_droite.vmax_ang*robot.roue_droite.rayon
    go(interface,grille, robot, distance, vitesse, dt)
    
    
if __name__ == "__main__":
    dt = 1/300
    largeur, hauteur = 300, 300
    bg = "white"
    interface = Interface("Simulation de déplacement du robot", largeur, hauteur, bg)

    dim_robot_x, dim_robot_y = int(largeur / 10), int(hauteur / 10)

    grille = Grille(largeur, hauteur, 5)
    capteur = Capteur(Vecteur(0, -1))
    robot = Robot("R", int(largeur/2), int(hauteur/2), dim_robot_x, dim_robot_y, capteur, Vecteur(0, -1), 10, 150, color="red")

    #--------------------- CREATION DES BOUTTONS DE COMMANDE ---------------------#
    interface.go_button = interface.creer_button("Avance", avance)
    interface.go_button.grid(row=5, column=0)
    
    interface.carre_button = interface.creer_button("Tracer carre", faire_carre)
    interface.carre_button.grid(row=6, column=0)
    
    interface.acc_no_coli_button = interface.creer_button("Acceleration sans colision", accelerer_sans_colision)
    interface.acc_no_coli_button.grid(row=7, column=0)
    
    update(interface, robot)

    interface.root.mainloop()