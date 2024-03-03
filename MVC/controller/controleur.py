from MVC.modele.robot import Robot, Vecteur
from time import sleep
import math

def calcul_dOM(robot: Robot, dt: float): 
    """ Calcul les dOM pour lezs utiliser lors de appel de go_dOM

    :param robot: Le robot qui va faire le deplacement 
    :param v_ang_d: La vitesse angulaire de la roue droite du robot en rad/s 
    :param v_ang_g: La vitesse angulaire de la roue gauche du robot en rad/s 
    :param dt: Le fps
    """
    dOM_theta = -robot.roue_droite.rayon*(robot.roue_droite.vitesse_angulaire+robot.roue_gauche.vitesse_angulaire)/robot.length * dt
    dOM_x = robot.vectDir.x*robot.vitesse()*dt #/robot.grille.echelle 
    dOM_y = robot.vectDir.y*robot.vitesse()*dt #/robot.grille.echelle 

    dOM = Vecteur(dOM_x, dOM_y)

    return dOM_theta, dOM_x, dOM_y, dOM

class Strategie():
    def __init__(self):
        pass
    
class Go(Strategie): 
    def __init__(self, robot: Robot, distance : int, v_ang_d: float, v_ang_g: float, dt: float) -> None:
        """/!!\\ robot ne comprends pas distance negative
        
        :param robot: Le robot qui va faire le deplacement 
        :param distance: La distance que le robot doit parcourir (float) 
        :param v_ang_d: La vitesse angulaire de la roue droite du robot en rad/s 
        :param v_ang_g: La vitesse angulaire de la roue gauche du robot en rad/s 
        :param dt: Le fps
        """
        super().__init__()  # Appel du constructeur de la classe parente 
        self.robot = robot
        self.distance = distance
        
        self.v_ang_d, self.v_ang_g = v_ang_d, v_ang_g

        #compteur de distance deja parcouru
        self.parcouru = 0

        #le fps
        self.dt = dt
       #print("x, y", robot.vectDir.x, robot.vectDir.y)
    
    def start(self, robot : Robot):
        """ Commencer la strategie
        """
        #actualiser la position du robot 
        self.robot = robot
        self.dOM_x = robot.vectDir.x*robot.vitesse()*self.dt #/robot.grille.echelle 
        self.dOM_y = robot.vectDir.y*robot.vitesse()*self.dt #/robot.grille.echelle 
        self.dOM = Vecteur(self.dOM_x, self.dOM_y)

        # Modifier les vitesses angulaire les roues
        self.robot.roue_droite.vitesse_angulaire = self.v_ang_d # Vitesse angulaire droite
        self.robot.roue_gauche.vitesse_angulaire = self.v_ang_g # Vitesse angulaire gauche
        #Calcul des dOM
        self.dOM_theta, self.dOM_x, self.dOM_y, self.dOM = calcul_dOM(self.robot, self.dt)

        #compteur de distance deja parcouru
        self.parcouru = 0      

    def stop(self):
        """ Savoir le parcour est fini ou non

        :return : Retourne vrai si on fini de parcourir la distance  
        """
        return self.parcouru > self.distance

    def step(self):
        """ Faire un deplacement de dOM 
        """
        #Incrémenter la distance parcourru
        self.parcouru += self.dOM.norme
        if self.stop(): 
            print("STOP")
            self.robot.roue_droite.vitesse_angulaire = 0
            self.robot.roue_gauche.vitesse_angulaire = 0
            return
        
        self.dOM_theta = 0
        #Bouger le robot d'un dOM
        if -self.v_ang_d != self.v_ang_g: #si veut tourner 
            #Calcul des dOM
            self.dOM_theta, self.dOM_x, self.dOM_y, self.dOM = calcul_dOM(self.robot, self.dt)
            #print(self.dOM_theta)
        self.robot.move_dOM(self.dOM_x, self.dOM_y, self.dOM_theta)

class Go_cap(Strategie): 
    def __init__(self, robot: Robot, distance : int, v_ang_d: float, v_ang_g: float, dt: float) -> None:
        """/!!\\ robot ne comprends pas distance negative
        
        :param robot: Le robot qui va faire le deplacement 
        :param distance: La distance que le robot doit parcourir (float) 
        :param v_ang_d: La vitesse angulaire de la roue droite du robot en rad/s 
        :param v_ang_g: La vitesse angulaire de la roue gauche du robot en rad/s 
        :param dt: Le fps
        """
        super().__init__()  # Appel du constructeur de la classe parente 
        self.robot = robot
        self.distance = distance
        
        self.v_ang_d, self.v_ang_g = v_ang_d, v_ang_g

        #compteur de distance deja parcouru
        self.parcouru = 0

        #le fps
        self.dt = dt
        #print("x, y", robot.vectDir.x, robot.vectDir.y)

    def start(self, robot : Robot):
        """ Commencer la strategie
        """
        #actualiser la position du robot 
        self.robot = robot
        self.dOM_x = robot.vectDir.x*robot.vitesse()*self.dt #/robot.grille.echelle 
        self.dOM_y = robot.vectDir.y*robot.vitesse()*self.dt #/robot.grille.echelle 
        self.dOM = Vecteur(self.dOM_x, self.dOM_y)

        # Modifier les vitesses angulaire les roues
        self.robot.roue_droite.vitesse_angulaire = self.v_ang_d  # Vitesse angulaire droite
        self.robot.roue_gauche.vitesse_angulaire = self.v_ang_g  # Vitesse angulaire gauche
        #Calcul des dOM
        self.dOM_theta, self.dOM_x, self.dOM_y, self.dOM = calcul_dOM(self.robot, self.dt)
        
        #compteur de distance deja parcouru
        self.parcouru = 0  
        #Verification de detection d'un mur ou obstacle     
        self.danger = self.robot.arene.raytracing(self.robot) < 2 

    def stop(self):
        """ Savoir le parcour est fini ou non

        :return : Retourne vrai si on fini de parcourir la distance  
        """
        return self.parcouru > self.distance or self.danger

    def step(self):
        """ Faire un deplacement de dOM 
        """
        #Incrémenter la distance parcourru
        self.parcouru += self.dOM.norme
        #Verification de detection d'un mur ou obstacle 
        self.danger = self.robot.arene.raytracing(self.robot) < 2 

        if self.stop(): 
            print("STOP")
            # Mettre à 0 les vitesses
            self.robot.roue_droite.vitesse_angulaire = 0
            self.robot.roue_gauche.vitesse_angulaire = 0
            return
        
        self.dOM_theta = 0
        #Bouger le robot d'un dOM
        if -self.v_ang_d != self.v_ang_g: #si veut tourner 
            #Calcul des dOM
            self.dOM_theta, self.dOM_x, self.dOM_y, self.dOM = calcul_dOM(self.robot, self.dt)
            #print(self.dOM_theta)

        self.robot.move_dOM(self.dOM_x, self.dOM_y, self.dOM_theta)

class Tourner_deg(Strategie): 
    def __init__(self, robot: Robot,  angle : int, v_ang: float, dt: float) -> None:
        """"
        :param robot: Le controleur qui donne l'ordre 
        :param angle: L'angle que le robot doit parcourir (float) 
        :param v_ang: La vitesse angulaire de la roue droite ou gauche du robot en rad/s 
        :param dt: Le fps
        """
        super().__init__()  # Appel du constructeur de la classe parente 
        self.angle = angle
        self.robot = robot

        self.v_ang = v_ang #Vitesse angulaire 
        self.parcouru = 0 #compteur de distance deja parcouru
        self.angle = angle #angle à parcourir
        self.dt = dt

        #Calcul des dOM
        self.dOM_theta, self.dOM_x, self.dOM_y, self.dOM = calcul_dOM(self.robot, self.dt)
        #print("x, y", robot.vectDir.x, robot.vectDir.y)

    def start(self, robot: Robot):
        """ Commencer la strategie
        """
        # Modifier les vitesses angulaire les roues
        if self.angle > 0:
            self.robot.roue_droite.vitesse_angulaire = -self.v_ang  # Vitesse angulaire droite
            self.robot.roue_gauche.vitesse_angulaire = 0  # Vitesse angulaire gauche
            self.v_ang_d, self.v_ang_g = -self.v_ang, 0
        else:
            self.robot.roue_droite.vitesse_angulaire = 0  # Vitesse angulaire droite
            self.robot.roue_gauche.vitesse_angulaire = self.v_ang 
            self.v_ang_d, self.v_ang_g = 0, self.v_ang

        #compteur de distance deja parcouru
        self.parcouru = 0      

    def stop(self):
        """ Savoir le parcours est fini ou non

        :return : Retourne vrai si on fini de parcourir la distance  
        """
        if self.angle > 0:
            return self.parcouru > self.angle
        else:
            return self.parcouru < self.angle

 
    def step(self):
        """ Faire un deplacement de dOM 
        """
        #Incrémenter la distance parcourru
        self.parcouru += (-self.robot.roue_droite.rayon*(self.robot.roue_droite.vitesse_angulaire+self.robot.roue_gauche.vitesse_angulaire)/self.robot.length * self.dt)*180/math.pi

        if self.stop(): 
            print("STOP")
            # Mettre à 0 les vitesses
            self.robot.roue_droite.vitesse_angulaire = 0
            self.robot.roue_gauche.vitesse_angulaire = 0
            return
        
        self.dOM_theta = 0
        #Bouger le robot d'un dOM
        if -self.v_ang_d != self.v_ang_g: #si veut tourner 
            self.dOM_theta, self.dOM_x, self.dOM_y, self.dOM = calcul_dOM(self.robot, self.dt)

        self.robot.move_dOM(0, 0, self.dOM_theta)
    
class Test_collision(Strategie):
    def __init__(self, robot : Robot, posX: float, posY: float,  distance : int, v_ang : float, dt: float):
        """Trace un carré

        :param robot: Le robot qui reçoit l'ordre
        :param posX: position en x de depart du robot 
        :param posY: position en y de depart du robot 
        :param vang: La vitesse angulaire des roues du robot
        :param distance: La distance que le robot parcours, dans notre cas longueur du carré
        :param dt: Le FPS
        """
        super().__init__()  # Appel du constructeur de la classe parente 
        
        self.robot = robot
        self.dt =dt
        self.strat = Go_cap(self.robot, distance, -v_ang, v_ang, dt)

        #Les listes des positions
        self.list_pos = [(posX+distance, posY), (posX, posY-distance), (posX-distance, posY), (posX, posY+distance)]

        self.cur = -1

    def start(self, robot: Robot):
        """ Commencer la strategie
        """
        self.robot.vectDir = Vecteur(0, -1)
        self.cur = -1

    def step(self):
        """Fait avancer le traçage du carré
        """
        if self.stop(): 
            print("STOP")
            # Mettre à 0 les vitesses
            self.robot.roue_droite.vitesse_angulaire = 0
            self.robot.roue_gauche.vitesse_angulaire = 0
            return
        #Avance d'une étape
        if self.cur <0 or self.strat.stop():
            self.cur+=1
            self.robot.vectDir = self.robot.vectDir.rotation(90)
            self.robot.posX, self.robot.posY = self.list_pos[self.cur]
            self.strat.start(self.robot)

        self.strat.step()
    
    def stop(self):
        """Vérifie si toutes les étapes sont terminées
        """
        return self.cur == len(self.list_pos)-1 and self.strat.stop()
    
class Controleur:
    def __init__(self, robot: Robot, dt: float):
        """
        Initialise le contrôleur avec un robot, une vue et un intervalle de temps.

        :param robot: Le robot
        :param dt: Le fps
        """
        # Modèle
        self.robot = robot
        
        # Vues 
        self.view = None

        # liste strat
        self.liste_strat = []

        self.cur = -1
        # Le fps
        self.dt = dt

    def reset_robot(self):
        """ Mettre robot au mileu du plan
        """
        self.robot.vectDir = Vecteur(0, -1)
        self.robot.posX, self.robot.posY = self.view.arene.maxX/2, self.view.arene.maxY /2

    def add_strat(self, strat: Strategie):
        """ Ajouter une strategie au conntroleur

        :param strat: Une strategie 
        """
        self.liste_strat.append(strat)

    def stop(self):
        """Vérifie si toutes les étapes sont terminées
        """
        if self.liste_strat == []: 
            return True
        return self.cur == len(self.liste_strat)-1 and self.liste_strat[self.cur].stop()
    
    def step(self):
        """Faire la commande suivante 
        """
        if self.stop(): 
            # Mettre à 0 les vitesses
            self.robot.roue_droite.vitesse_angulaire = 0
            self.robot.roue_gauche.vitesse_angulaire = 0
            return
        #Faire la strtégie suivante 
        if self.cur <0 or self.liste_strat[self.cur].stop():
            self.cur+=1
            self.liste_strat[self.cur].start(self.robot)
        print(self.cur)
        self.liste_strat[self.cur].step()

    def tracer_carre(self ,distance : int,v_ang : float ,dt : float):
        """Trace un carré
        :param distance: La distance que le robot parcours, dans notre cas longueur du carré
        :param vang: La vitesse angulaire des roues du robot
        :param dt: Le FPS
        """
        for i in range(4):
            self.add_strat(Go(self.robot, distance, -v_ang, v_ang, dt));
            self.add_strat(Tourner_deg(self.robot, 90, v_ang, dt));

    def go_cap_vmax(self, distance : int, dt: float):
        """
        Avance avec le capteur et la vitesse maximale du robot
        :param distance: La distance que le robot parcours
        :param dt: Le fps
        """
        