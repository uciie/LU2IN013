from time import sleep
from modele.robot import *
from view.affichage import *
import math
class Controleur:
    def __init__(self, robot: Robot, dt):
        """
        Initialise le contrôleur avec un robot, une vue et un intervalle de temps.

        :param robot: Le robot
        :param dt: Le fps
        """
        # Modèle
        self.robot = robot
        
        # Vues 
        self.view = None

        self.dt = dt

    def set_view(self, view: Affichage):
        """ L'ajout du View dans le controller
        
        :param view: Le module View
        """
        if self.view : 
            self.reset_robot()
            self.view.root.destroy()  # Destroy the current window
        self.view = view
        self.view.set_controller(self)

    def reset_robot(self):
        """ Mettre robot au mileu du plan
        """
        self.robot.vectDir = Vecteur(0, -1)
        self.robot.posX, self.robot.posY = self.view.arene.maxX/2, self.view.arene.maxY /2

    def go(self, distance, v_ang_d, v_ang_g):
        """ Faire avancer le robot 
        
        :param distance: La distance que le robot doit parcourir (float) 
        :param v_ang_d: La vitesse angulaire de la roue droite du robot en rad/s 
        :param v_ang_g: La vitesse angulaire de la roue gauche du robot en rad/s 
        """
        print("avant GO\n")
        mouvement = Go(self.robot,distance, v_ang_d, v_ang_g, self.dt)

        # Boucle pour avancer le robot jusqu'à ce qu'il atteigne la distance spécifiée
        d = self.robot.capteur.raytracing(self.robot, self.view.arene.maxX, self.view.arene.maxY)
        while not mouvement.stop() or d = 0:
            d = self.robot.capteur.raytracing(self.robot, self.view.arene.maxX, self.view.arene.maxY)
            mouvement.step()
            print(self.robot.posX, self.robot.posY, self.robot.roue_droite.vitesse_angulaire, self.robot.roue_gauche.vitesse_angulaire)
            if self.view: # si on a un module View
                self.view.update()
            sleep(self.dt)


class Tourner(): 
    def __init__(self, controleur : Controleur, angle : int, v_ang, dt) -> None:
        """
        
        :param controleur: Le controleur qui donne l'ordre 
        :param angle: L'angle que le robot doit parcourir (float) 
        :param v_ang: La vitesse angulaire de la roue droite ou gauche du robot en rad/s 
        :param dt: Le fps
        """
        self.controleur = controleur
        self.angle = angle

        # Modifier les vitesses angulaire les roues
        if angle > 0:
            self.controleur.robot.roue_droite.set_vitesse_angulaire(v_ang)  # Vitesse angulaire droite
            self.controleur.robot.roue_gauche.set_vitesse_angulaire(0)  # Vitesse angulaire gauche
            self.v_ang_d, self.v_ang_g = v_ang, 0
        else:
            self.controleur.robot.roue_droite.set_vitesse_angulaire(0)  # Vitesse angulaire droite
            self.controleur.robot.roue_gauche.set_vitesse_angulaire(v_ang) 
            self.v_ang_d, self.v_ang_g = 0, v_ang

        #compteur d'angle deja parcouru
        self.parcouru = 0

        #Coordonnee de vecteur de deplacement 
        self.dOM_x = controleur.robot.vectDir.x*robot.vitesse()*dt #/robot.grille.echelle 
        self.dOM_y = controleur.robot.vectDir.y*robot.vitesse()*dt #/robot.grille.echelle 

        self.dOM = Vecteur(self.dOM_x, self.dOM_y)

        self.dt = dt
        print("x, y", robot.vectDir.x, robot.vectDir.y)
        print(self.angle, self.v_ang_d, self.v_ang_g, self.dOM_x, self.dOM_y)

    def stop(self):
        """ Savoir le parcours est fini ou non

        :return : Retourne vrai si on fini de parcourir la distance  
        """
        return self.parcouru > self.angle

    def step(self):
        """ Faire un deplacement de dOM 
        """
        #Incrémenter la distance parcourru
        self.parcouru += self.dOM_theta
        if self.stop(): return
        
        self.dOM_theta = 0
        #Bouger le robot d'un dOM
        if -self.v_ang_d != self.v_ang_g: #si veut tourner 
            self.dOM_theta = -self.robot.roue_droite.rayon*(self.v_ang_g+self.v_ang_d)/self.robot.length * self.dt
            self.dOM_x = self.robot.vectDir.x*self.robot.vitesse()*self.dt #/robot.grille.echelle 
            self.dOM_y = self.robot.vectDir.y*self.robot.vitesse()*self.dt #/robot.grille.echelle 

            self.dOM = Vecteur(self.dOM_x, self.dOM_y)

            print(self.dOM_theta)
        self.robot.move_dOM(self.dOM_x, self.dOM_y, self.dOM_theta)

