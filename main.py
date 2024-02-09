from controller.controleur import *
from view.affichage import *
from modele.arene import *
from modele.robot import *

class App():
    def __init__(self):
        dt = 1/300
        echelle = 5
        largeur, hauteur = 300, 300
        dim_robot_x, dim_robot_y = int(largeur / 10), int(hauteur / 10)

        # initilisation de l'arene et robot
        arene = Arene("Simulation de déplacement du robot", largeur, hauteur, echelle)
        robot = Robot("R", int(largeur/2), int(hauteur/2), dim_robot_x, dim_robot_y, 10, 150, color="red")
        
        # ajouter un robot dans l'arene 
        arene.addRobot(robot)

        #Creation du module View
        view = False #Affichage(arene)

        #Creation du module Controller
        controller = Controleur(robot, dt)

        # Ajoute du lien de communication entre controller et view
    
        # Ajoute du lien de communication entre view et controller 
        if view :
            controller.set_view(view)
            view.set_controller(controller)
            view.root.mainloop()
        else :
            controller.go(10, 10, -10)

if __name__ == '__main__':
    app = App()