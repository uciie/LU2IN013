import threading

<<<<<<< HEAD
from MVC.controller.adaptateur_robot_irl import AdaptateurRobotIrl
from MVC.controller.ai import Go, TournerDeg
from MVC.controller.controleur import Controleur
from MVC.robot.robot2I013 import Robot2IN013

=======
from MVC.controller.controleur import Controleur, AdaptateurRobotIrl
from MVC.robot.robot2I013 import Robot2IN013

from MVC.controller.ai import Go, TournerDeg

>>>>>>> test_robot_irl

def main():
    # Création du verrou

    dt_controller = 1 / 1000

    # Initialisation de l'arene, robot, obstacle
    robot = Robot2IN013()

    # Créer l'adaptateur
    adaptateur = AdaptateurRobotIrl(robot)

    # Création du module Controller
    controller = Controleur(adaptateur, dt_controller,)

    # Avancer
    strat1 = Go(controller.adaptateur, 50, 50, 50, controller.dt)
    controller.add_strat(strat1)

    # Tourner
    strat2 = TournerDeg(controller.adaptateur, 90, 10, controller.dt)
    controller.add_strat(strat2)

    controller.start()
    controller.join()


if __name__ == '__main__':
    main()
