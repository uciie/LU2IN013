from controller.controleur import Controleur
from view.affichage import Affichage
from modele.arene import Arene
from modele.robot import Robot
from modele.obstacle import Obstacle
from modele.vecteur import Vecteur
import time 

class App():
    def __init__(self):
        self.dt = 1/500
        echelle = 5
        largeur, hauteur = 500, 500
        dim_robot_x, dim_robot_y = int(largeur / 10), int(hauteur / 10)


        # initilisation de l'arene et robot
        self.arene = Arene("Simulation de déplacement du robot", largeur, hauteur, echelle)
        self.robot = Robot("R", int(largeur/2), int(hauteur/2), dim_robot_x, dim_robot_y, 10, 150, color="red")
        obs = Obstacle(30, 50, Vecteur(10, 0), Vecteur(0,20), Vecteur(10, 0), Vecteur(0,20))
        
        # ajouter un robot dans l'arene 
        self.arene.addRobot(self.robot)

        self.arene.addObstacle(obs)

        #Creation du module View
        self.view = Affichage(self.arene)

        #Creation du module Controller
        self.controller = Controleur(self.robot, self.dt)

        # Ajoute du lien de communication entre controller et view
    
        # Ajoute du lien de communication entre view et controller 
        if self.view :
            self.view.set_controller(self.controller)
            self.runCtrl()
            self.view.root.mainloop()
        # si View n'existe pas 
        else :
            self.controller.go(10, 10, -10)

    def runCtrl(self):
        while True:
            self.controller.step()
            if self.view is not None:
                self.view.update()
            

if __name__ == '__main__':
    app = App()