from MVC.modele.vecteur import Vecteur
from MVC.modele.robot.robot_mere import Robot_mere
from MVC.modele.robot.robot_fils import Robot
from time import sleep

class Strategie():
    def __init__(self):
        pass
    
class Go(Strategie): 
    def __init__(self, robot: Robot_mere, distance : int, v_ang_d: float, v_ang_g: float, dt: float) -> None:
        """/!!\\ robot ne comprends pas distance negative
        Fait avancer le robot d'une certaine distance
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
    
    def start(self, robot : Robot_mere):
        """ Commencer la strategie
        """
        #actualiser la position du robot 
        self.robot = robot

        # Modifier les vitesses angulaire les roues
        self.robot.set_vitesse_roue(self.v_ang_d, self.v_ang_g) # Vitesse angulaire droite/gauche

        if isinstance(robot, Robot) : 
            #Calcul des dOM
            self.dOM_theta, self.dOM_x, self.dOM_y= self.robot.calcul_dOM(self.dt)
            self.dOM = Vecteur(self.dOM_x, self.dOM_y)

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
            # Mettre à 0 les vitesses
            self.robot.stop() # Vitesse angulaire droite/gauche
            return
        
        self.dOM = self.robot.step(self.dOM_x, self.dOM_y, self.dt)

class Controleur:
    def __init__(self, robot: Robot_mere, dt: float):
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
            self.robot.stop() # Vitesse angulaire droite/gauche
            return
        #Faire la strtégie suivante 
        if self.cur <0 or self.liste_strat[self.cur].stop():
            self.cur+=1
            self.liste_strat[self.cur].start(self.robot)
        #print(self.cur)
        self.liste_strat[self.cur].step()

    def tracer_carre(self ,distance : int,v_ang : float ,dt : float):
        """Trace un carré
        :param distance: La distance que le robot parcours, dans notre cas longueur du carré
        :param vang: La vitesse angulaire des roues du robot
        :param dt: Le FPS
        """

        #Ajoute les stratégies pour faire un carré
        for i in range(4):
            self.add_strat(Go(self.robot, distance, -v_ang, v_ang, dt))
            self.add_strat(Tourner_deg(self.robot, 90, v_ang, dt))

    def go_cap_vmax(self, distance : int, dt: float):
        """
        Avance avec le capteur et la vitesse maximale du robot
        :param distance: La distance que le robot parcours
        :param dt: Le fps
        """
        #Ajoute la stratégie Go_cap avec la vitesse maximale du robot
        self.add_strat(Go_cap(self.robot, distance, -self.robot.roue_droite.vmax_ang, self.robot.roue_gauche.vmax_ang, dt))