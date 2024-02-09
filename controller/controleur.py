from time import sleep
from modele.robot import *
from view.affichage import *

class Controleur:
    def __init__(self, robot: Robot, view: Affichage, dt):
        """
        Initialise le contrôleur avec un robot, une vue et un intervalle de temps.
        """
        # Modèle
        self.robot = robot
        
        # Vues 
        self.view = view

        self.dt = dt

    def go(self, distance, v_ang_d, v_ang_g):
        """ Faire avancer le robot 
        :param:
        """
        print("avant GO\n")
        mouvement = Go(self.robot,distance, v_ang_d, v_ang_g, self.dt)

        # Boucle pour avancer le robot jusqu'à ce qu'il atteigne la distance spécifiée
        while not mouvement.stop():
            mouvement.step()
            print(self.robot.posX, self.robot.posY, self.robot.roue_droite.vitesse_angulaire, self.robot.roue_gauche.vitesse_angulaire)
            #self.view.update()
            sleep(self.dt)
