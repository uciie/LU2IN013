from .modele.robot import Robot
from .modele.vecteur import Vecteur

class Controleur():
    def __int__(self):
        """
        """
        # Modele
        self.robot = None
        self.arene = None
        
        # Views 
        self.views = None

    def get_robot(self):
        """Demander à la View d'ajouter un robot
        """
        largeur, hauteur = 300, 300
        dim_robot_x, dim_robot_y = int(largeur / 10), int(hauteur / 10)
        self.robot = Robot("R", int(largeur/2), int(hauteur/2), dim_robot_x, dim_robot_y, capteur, Vecteur(0, -1), 10, 150, color="red"))

    def go(self, distance, v_ang_d, v_ang_g):
        """ Faire avancer le robot 
        :param:
        """
        



    def run(self, fps = 300): 
        self.get_robot()

        running = True
        while running : 
            if self.arene is not None : 
                self.arene.update()
            if self.views is not None : 
                self.views.affichage()
