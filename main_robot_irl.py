import threading
from src.controller.adaptateur_robot_irl import AdaptateurRobotIrl
from src.controller.controleur import Controleur
import time
import logging
try:
    from robot2IN013 import Robot2IN013
except ModuleNotFoundError:
    from src.robot.robot2I013Fake import Robot2IN013

from src.controller.ai import Go, StrategieSequentielle, TournerDeg, StrategieIf, StrategieWhile, Stop
from strategies_prefaites import test_strat_seq_carre, test_go_sans_tracer, test_while, test_tourner90, test_if

# Configure logging to write to both terminal and file
logging.basicConfig(level=logging.DEBUG, filename='logs/cam.log', filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Créer un gestionnaire pour afficher les messages dans le terminal
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Définir le niveau de logging pour la sortie terminal
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

logger = logging.getLogger(__name__)

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
    stop = Stop(demo.controller.adaptateur)
    strat = StrategieWhile(demo.controller.adaptateur, test_go_sans_tracer, 10)
    demo.controller.add_strat(strat)
