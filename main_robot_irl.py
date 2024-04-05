import threading
from src.controller.adaptateur_robot_irl import AdaptateurRobotIrl
from src.controller.controleur import Controleur

try:
    from robot2IN013 import Robot2IN013
except ModuleNotFoundError:
    from src.robot.robot2I013Fake import Robot2IN013

from src.controller.ai import Go, StrategieSequentielle, TournerDeg, StrategieIf, StrategieWhile
from strategies_prefaites import test_strat_seq_carre, test_go_sans_tracer, test_while, test_tourner90

class DemoIrl:
    def __init__(self):
        # Création du verrou

        dt_controller = 1 / 1000

        # Initialisation de l'_arene, robot, obstacle
        self.robot = Robot2IN013()

        # Créer l'adaptateur
        self.adaptateur = AdaptateurRobotIrl(self.robot)

        # Création du module Controller
        self.controller = Controleur(self.adaptateur, dt_controller)

        self.controller.start()

if __name__ == '__main__':
    demo = DemoIrl()
    go = test_go_sans_tracer(demo.controller)
    strat = StrategieWhile(demo.controller.adaptateur, go , 100)
    demo.controller.add_strat(strat)
