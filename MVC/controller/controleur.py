import math
import threading
import time
from abc import ABC, abstractmethod
from threading import Thread

from ..modele.objets import SimuRobot
from ..modele.simulation import Simulation
from ..modele.vecteur import Vecteur
from ..robot.robot2I013 import Robot2IN013


class Adaptateur(ABC):
    def __init__(self) -> None:
        """
        """
        self._v_ang_roue_d = 0
        self._v_ang_roue_g = 0

    @property
    def v_ang_d(self) -> float:
        """ Obtenir la vitesse angulaire de la route droite
        """
        return self._v_ang_roue_d

    @v_ang_d.setter
    def v_ang_d(self, value: float):
        self._v_ang_roue_d = value

    @property
    def v_ang_g(self) -> float:
        """ Obtenir la vitesse angulaire de la route droite
        """
        return self._v_ang_roue_g

    @v_ang_g.setter
    def v_ang_g(self, value: float):
        self._v_ang_roue_g = value

    @abstractmethod
    def set_vitesse_roue(self, v_ang_roue_d: float, v_ang_roue_g: float):
        """ Modifier la vitesse des roues
        """
        pass

    @property
    @abstractmethod
    def vitesse_ang_roues(self) -> tuple[float, float]:
        """ Obtenir la vitesse angulaire des roues
        """
        pass

    @property
    @abstractmethod
    def distance_parcourue(self):
        """ Obtenir la distance parcourue
        """
        pass

    @property
    @abstractmethod
    def angle_parcourue(self):
        """ Obtenir l'angle parcouru
        """
        pass

    @property
    @abstractmethod
    def stop(self):
        """ Arreter le robot
        """
        pass

    @property
    @abstractmethod
    def robot(self):
        """
        """
        pass

    @abstractmethod
    def actualiser(self):
        """Actualiser la simulation
        """
        pass


class AdaptateurRobotSimu(Adaptateur):
    def __init__(self, robot: SimuRobot, simulation: Simulation):
        """
        """
        super().__init__()
        self._robot = robot
        self._simulation = simulation

        self.last_theta = self._robot.last_theta
        self.last_pos_x, self.last_pos_y = self._robot.last_pos_x, self._robot.last_pos_y

    @property
    def robot(self):
        return self._robot

    def set_vitesse_roue(self, v_ang_roue_d: float, v_ang_roue_g: float):
        """ Modifier la vitesse des roues

        :param v_ang_roue_d: Modifier la vitesse angulaire de la roue droite
        :param v_ang_roue_g: Modifier la vitesse angulaire de la roue gauche
        """
        self.robot.set_vitesse_roue(v_ang_roue_d, v_ang_roue_g)

    @property
    def distance_parcourue(self) -> float:
        """ Obtenir la distance parcourue
        :return: la distance parcourue
        """
        distance = Vecteur(self._robot.pos_x - self.last_pos_x, self._robot.pos_y - self.last_pos_y)
        self.last_pos_x, self.last_pos_y = self._robot.pos_x, self._robot.pos_y
        return distance.norme

    @property
    def angle_parcourue(self) -> float:
        """ Obtenir l'angle parcouru
        :return: l'angle parcouru
        """
        angle = self._robot.theta - self.last_theta
        self.last_theta = self._robot.theta
        return angle

    def stop(self):
        """ Arreter le robot irl
        :return: True si le robot est en arret
        """
        self.set_vitesse_roue(0, 0)

    @property
    def vitesse_ang_roues(self) -> tuple[float, float]:
        """ Obtenir la vitesse angulaire des roues droite et gauche
        :return: la vitesse angulaire des roues
        """
        return self._robot.roue_droite.vitesse_angulaire, self._robot.roue_gauche.vitesse_angulaire

    def actualiser(self):
        """Actualiser la simulation
        """
        #self._simulation.update()
        pass


class AdaptateurRobotIrl(Adaptateur):
    def __init__(self, robot: Robot2IN013):
        """ Adaptateur du robot irl
        """
        super().__init__()
        self._robot = robot
        self._v_ang_roue_d, self._v_ang_roue_g = 0., 0.

    @property
    def v_ang_d(self) -> float:
        return self._v_ang_roue_d

    @v_ang_d.setter
    def v_ang_d(self, v_ang_roue_d: float):
        self._v_ang_roue_d = v_ang_roue_d

    @property
    def v_ang_g(self) -> float:
        return self._v_ang_roue_g

    @v_ang_g.setter
    def v_ang_g(self, v_ang_roue_g: float):
        self._v_ang_roue_g = v_ang_roue_g

    @property
    def robot(self):
        return self._robot

    def set_vitesse_roue(self, v_ang_roue_d: float, v_ang_roue_g: float):
        """ Modifier la vitesse des roues

        :param v_ang_roue_d: Modifier la vitesse angulaire de la roue droite
        :param v_ang_roue_g: Modifier la vitesse angulaire de la roue gauche
        """
        self._v_ang_roue_d = v_ang_roue_d
        self._v_ang_roue_g = v_ang_roue_g
        self._robot.set_motor_dps("roue_droite", v_ang_roue_d)
        self._robot.set_motor_dps("roue_gauche", v_ang_roue_g)

    @property
    def distance_parcourue(self):
        """ Obtenir la distance parcourue
        :returns : Renvoie la distance parcourue du robot
        """
        return self.angle_parcourue / 360 * self._robot.WHEEL_DIAMETER * 2 * math.pi

    @property
    def angle_parcourue(self):
        """ Obtenir l'angle parcouru
        :returns : Renvoie l'angle parcourut du robot en degree
        """
        # obtenir la position des angles des roues
        # pos_roues_x, pos_roues_y = self._robot.get_motor_position()
        # moyenne d'angle parcourue
        # angle_parcourue = (pos_roues_x + pos_roues_y) / 2

        # self._robot.offset_motor_encoder("roue_droite", 0)
        # self._robot.offset_motor_encoder("roue_gauche", 0)
        angle_parcourue = 1
        return angle_parcourue

    def stop(self):
        """ Arreter le robot irl
        """
        self.set_vitesse_roue(0, 0)

    def actualiser(self):
        """"""
        self.set_vitesse_roue(self._v_ang_roue_d, self._v_ang_roue_g)
        print(self.info)

    @property
    def vitesse_ang_roues(self) -> tuple[float, float]:
        """ Obtenir la vitesse angulaire des roues droite et gauche
        :return: la vitesse angulaire des roues
        """
        return self._v_ang_roue_d, self._v_ang_roue_g

    @property
    def info(self) -> str:
        """ afficher les informations du robot
        :return str: informations du robot
        """
        info_str = ""
        info_str += f"Vitesse roue droite: {self._v_ang_roue_d}\n"
        info_str += f"Vitesse roue gauche: {self._v_ang_roue_g}\n"
        return info_str


class Strategie(ABC):
    def __init__(self):  # , adaptateur: Adaptateur):
        """ Initialise la classe Strategie
        """
        # self._adaptateur = adaptateur

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self) -> bool:
        pass

    @abstractmethod
    def step(self):
        pass


class Controleur(Thread):
    def __init__(self, adaptateur: Adaptateur, dt: float, lock: threading.RLock):
        """
        Initialise le contrôleur avec un robot, une vue et un intervalle de temps.

        :param adaptateur: Le robot
        :param dt: Le fps
        """
        super(Controleur, self).__init__()
        # Modèle
        self.adaptateur = adaptateur

        # Vues 
        self.view = None

        # liste strat
        self.liste_strat = []

        self.cur = -1
        # Le fps
        self.dt = dt
        self.lock = lock
        self._running = False

    def add_strat(self, strat: Strategie):
        """ Ajouter une strategie au conntroleur

        :param strat: Une strategie
        """
        self.liste_strat.append(strat)

    def stop(self):
        """Vérifie si toutes les étapes sont terminées
        """
        if not self.liste_strat:
            return True
        return self.cur == len(self.liste_strat) - 1 and self.liste_strat[self.cur].stop()

    def run(self):

        self._running = True
        while self._running:
            start_time = time.time()
            self.step()
            end_time = time.time() - start_time
            sleep_time = max(0., self.dt - end_time)
            time.sleep(sleep_time)


    def step(self):
        """Faire la commande suivante"""
        with self.lock:
            if self.stop():
                return
            # Faire la stratégie suivante
            if self.cur < 0 or self.liste_strat[self.cur].stop():
                self.cur += 1
                print(self.cur)
                self.liste_strat[self.cur].start()
            self.liste_strat[self.cur].step()
