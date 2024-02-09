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

        arene = Arene("Simulation de déplacement du robot", largeur, hauteur, echelle)

        robot = Robot("R", int(largeur/2), int(hauteur/2), dim_robot_x, dim_robot_y, 10, 150, color="red")
        arene.addRobot(robot)

        self.view = Affichage(arene)
        controller = Controleur(robot, self.view, dt)
    
        controller.go(100, -10, 10)
        self.view.set_controller(controller)
        self.view.root.mainloop()

        

if __name__ == '__main__':
    app = App()
    #app.mainloop()  