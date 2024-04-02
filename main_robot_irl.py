import threading

from src.controller.adaptateur_robot_irl import AdaptateurRobotIrl
from src.controller.controleur import Controleur
from robot2IN013 import Robot2IN013
from strategies_prefaites import *
from src.controller.ai import Go, TournerDeg, StrategieSequentielle, StrategieWhile, StrategieIf


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
    strat1 = Go(controller.adaptateur, 100, 50, 50)
    #controller.add_strat(strat1)

    # Tourner
    strat2 = TournerDeg(controller.adaptateur, 90, 50)
    #controller.add_strat(strat2)

    l_strat = [StrategieSequentielle(adaptateur, [strat1,strat2]) for _ in range(4)]
    strat = StrategieSequentielle(adaptateur, l_strat)
    controller.add_strat(strat)

    #controller.add_strat(test_strat_seq_carre)
    controller.start()
    controller.join()


if __name__ == '__main__':
    main()
