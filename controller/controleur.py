from time import sleep
from modele.robot import *
from view.affichage import *
from .strategies import * 
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

        #Savoir si on a un obstacle devant robot
        d = self.robot.capteur.raytracing(self.robot, self.view.arene.maxX, self.view.arene.maxY)

        # Boucle pour avancer le robot jusqu'à ce qu'il atteigne la distance spécifiée
        while not mouvement.stop() and d > 1:
            d = self.robot.capteur.raytracing(self.robot, self.view.arene.maxX, self.view.arene.maxY)
            mouvement.step()
            print(self.robot.posX, self.robot.posY, self.robot.roue_droite.vitesse_angulaire, self.robot.roue_gauche.vitesse_angulaire)
            if self.view: # si on a un module View
                self.view.update()
            sleep(self.dt)

    def tourner(self, angle, v_ang):
        """ Faire tourner le robot
        :param angle: L'angle que le robot doit parcourir (float)
        :param v_ang: La vitesse angulaire de la roue gauche ou droite en rad/s
        """
        if (angle > 0):
            print("gauche GO\n")
        else:
            print("droite GO\n")
        mouvement = Tourner_deg(self.robot, angle, v_ang, self.dt)

        #Savoir si on a un obstacle devant robot
        d = self.robot.capteur.raytracing(self.robot, self.view.arene.maxX, self.view.arene.maxY)

        #Boucle pour tourner le robot jusqu'à ce qu'il ateingne l'angle spécifiée
        while not mouvement.stop() or d == 0:
            d = self.robot.capteur.raytracing(self.robot, self.view.arene.maxX, self.view.arene.maxY)
            mouvement.step()
            print(self.robot.posX, self.robot.posY, self.robot.roue_droite.vitesse_angulaire, self.robot.roue_gauche.vitesse_angulaire)
            if self.view: # si on a un module View
                self.view.update()
            sleep(self.dt)
    
    def tracer_carre(self, distance, v_ang):
        """Tracer un carré avec le robot
        :param distance: La distance que le robot doit parcourir
        :param v_ang : La vitesse angulaire des roues du robot
        """

        mouvement = Tracer_carre(self.robot, distance, v_ang, self.dt)

        while not mouvement.stop():
            #if mouvement.etapes[mouvement.cur]
            mouvement.step()
            #print(self.robot.posX, self.robot.posY, self.robot.roue_droite.vitesse_angulaire, self.robot.roue_gauche.vitesse_angulaire)
            if self.view: # si on a un module View
                self.view.update()
            sleep(self.dt)
