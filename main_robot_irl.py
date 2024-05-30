import threading
from src.controller.adaptateur_robot_irl import AdaptateurRobotIrl
from src.controller.controleur import Controleur
#deactivate logging
import logging
logging.disable(logging.CRITICAL)

try:
    from robot2IN013 import Robot2IN013
except ModuleNotFoundError:
    from src.robot.robot2I013Fake import Robot2IN013

from src.controller.ai import Go, StrategieSequentielle, TournerDeg, StrategieIf, StrategieWhile, Stop
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
    distance = 50
    vitesse = 50
    seuil_collision = 50
    avancer = Go(demo.controller.adaptateur, distance, vitesse, vitesse, True)
    strat = StrategieWhile(demo.adaptateur, avancer, seuil_collision)
    demo.controller.add_strat(go)
