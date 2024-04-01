import threading

from src.controller.adaptateur_robot_irl import AdaptateurRobotIrl
from src.controller.controleur import Controleur
from src.robot.robot2I013 import Robot2IN013

from src.controller.ai import Go, TournerDeg


def main():
    # Création du verrou

    dt_controller = 1 / 1000

    # Initialisation de l'_arene, robot, obstacle
    robot = Robot2IN013()

    # Créer l'adaptateur
    adaptateur = AdaptateurRobotIrl(robot)

    # Création du module Controller
    controller = Controleur(adaptateur, dt_controller)

    # Avancer
    strat1 = Go(controller.adaptateur, 50, 50, 50)
    controller.add_strat(strat1)

    # Tourner
    strat2 = TournerDeg(controller.adaptateur, 90, 10)
    #controller.add_strat(strat2)

    controller.start()
    controller.join()


if __name__ == '__main__':
    main()
