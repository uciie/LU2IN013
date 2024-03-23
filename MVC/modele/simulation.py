import sys
import threading
import time
import logging
from threading import Thread

from .objets import Arene, SimuRobot

# Configure logging
logging.basicConfig(level=logging.INFO, filename='logs/simu.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# Désactiver tous les messages de journalisation
#logging.getLogger('MVC.modele.simulation').setLevel(logging.WARNING)

class Simulation(Thread):
    """ Simulation class
    """

    def __init__(self, name: str, fps: float, robot: SimuRobot, arene: Arene, lock_aff: threading.RLock):
        """ Initialisation d'une simulation

        :param name: le nom de la simulation
        :param fps: le dt
        :param robot: Le robot 
        :param arene: L'arene
        """
        super(Simulation, self).__init__()
        self.name = name
        self._running = False
        self._robot = robot
        self._arene = arene
        self.dt = fps

        self.lock_aff = lock_aff
        self.logger = logging.getLogger(__name__)

    @property
    def running(self) -> bool:
        """ Retourne si la simulation tourne
        """
        return self._running

    @property
    def robot(self) -> SimuRobot:
        """ Retourne le robot
        """
        return self._robot

    @property
    def arene(self) -> Arene:
        """ Retourne l'arene
        """
        return self._arene

    def add_robot(self, robot: SimuRobot):
        """ Ajouter un robot dans la simulation
        """
        if not self._robot:
            self._robot = robot

    def remove_robot(self):
        """ Retirer le robot 
        """
        self._robot = None

    def stop(self):
        """ Arreter la simulation
        """
        self._running = False

    def run(self):
        """ Activer la simulation
        """
        self._running = True
        while self._running:
            start_time = time.time()  # Temps initial de l'itération
            self.update()
            end_time = time.time() - start_time
            sleep_time = self.dt - end_time
            self.logger.info(f"temps utilise {end_time}")
            if sleep_time < 0:
                self.dt = -sleep_time
                sleep_time = 0
            time.sleep(sleep_time)


    def update(self):
        """ Actualiser l'arene selon le dt ecoule
        """

        with self.lock_aff:
            # Actualiser le robot
            self._robot.actualiser(self.dt)
            self.logger.info(self._robot.info())

        # Verifier si le robot a crash avec un obstacle
        for obstacle in self._arene.liste_Obstacles:
            if obstacle.test_collision(self._robot):
                self._robot.set_vitesse_roue(0, 0)
                sys.exit()
                # self.remove_robot()

        # Verifier si le robot a crash sur un mur
        if self._robot.test_crash(self._arene.max_x, self._arene.max_y):
            self._robot.set_vitesse_roue(0, 0)
            sys.exit()
            # self.remove_robot()
        # end_time = time.time()  # Temps final de l'itération
        # self._fps = end_time - start_time  # Temps écoulé pour cette itération
        # time.sleep(1 / self._wait)
