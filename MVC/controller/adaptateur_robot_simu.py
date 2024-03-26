import logging

from MVC.controller.controleur import Adaptateur
from MVC.modele.objets import SimuRobot
from MVC.modele.simulation import Simulation
from MVC.modele.vecteur import Vecteur

# Configure logging
logging.basicConfig(level=logging.DEBUG, filename='logs/simu.log', filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# Désactiver les messages de journalisation pour le module spécifié
# logging.getLogger('MVC.controller.ai').setLevel(logging.WARNING)

class AdaptateurRobotSimu(Adaptateur):
    """Classe de l'adaptateur d'un robot simule '"""

    def __init__(self, robot: SimuRobot, simulation: Simulation):
        """ initialise la classe adaptateur_robot_simu
        :param robot: Robot simule
        :param simulation: Simulation robot arene
        """
        super().__init__()
        self._robot = robot
        self._simulation = simulation

        self._last_theta = self._robot.last_theta
        self._last_pos_x, self._last_pos_y = self._robot.last_pos_x, self._robot.last_pos_y
        self.logger = logging.getLogger(__name__)

    @property
    def last_theta(self) -> float:
        """Getter dernier tetha enregistre depuis le dernier appel
        :return float: l'angle theta du robot'"""
        return self._last_theta

    @last_theta.setter
    def last_theta(self, theta: float):
        """setter du dernier angle theta enregistre depuis le dernier appel
        :param float theta: nouveau angle theta '"""
        self._last_theta = theta

    @property
    def last_pos_x(self) -> float:
        """Getter de la derniere position en x enregistree depuis le dernier appel
        :return float: derniere position en x enregistree"""
        return self._last_pos_x

    @last_pos_x.setter
    def last_pos_x(self, x: float):
        """Setter de la derniere position en x enregistree
        :param float x: nouvelle position"""
        self._last_pos_x = x

    @property
    def last_pos_y(self) -> float:
        """Getter de la derniere position en y enregistree depuis le dernier appel
        :return float: derniere position en y enregistree"""
        return self._last_pos_y

    @last_pos_y.setter
    def last_pos_y(self, y: float):
        """Setter de la derniere position en y enregistree
        :param float y: nouvelle position"""
        self._last_pos_y = y

    @property
    def robot(self):
        return self._robot

    @property
    def simulation(self):
        return self._simulation

    def set_vitesse_roue(self, v_ang_roue_d: float, v_ang_roue_g: float):
        """ Modifier la vitesse des roues

        :param v_ang_roue_d: Modifier la vitesse angulaire de la roue droite
        :param v_ang_roue_g: Modifier la vitesse angulaire de la roue gauche
        """
        self._robot.set_vitesse_roue(v_ang_roue_d, v_ang_roue_g)

    @property
    def distance_parcourue(self) -> float:
        """ Obtenir la distance parcourue
        :return: la distance parcourue
        """
        distance = Vecteur(self._robot.pos_x - self._last_pos_x, self._robot.pos_y - self._last_pos_y)
        self._last_pos_x, self._last_pos_y = self._robot.pos_x, self._robot.pos_y
        return distance.norme

    @property
    def angle_parcourue(self) -> float:
        """ Obtenir l'angle parcouru
        :return: l'angle parcouru
        """
        angle_parcouru = self._robot.theta - self._last_theta
        # Ajustement de l'angle parcouru selon le sens trigonométrique ou horloge
        if angle_parcouru < -180:
            angle_parcouru += 360
        elif angle_parcouru > 180:
            angle_parcouru -= 360
        self._last_theta = self._robot.theta
        return angle_parcouru

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
        # self._simulation.update()
        pass

    def active_trace(self, val: bool):
        """Activer ou désactiver le tracage du robot."""
        self._robot.activer_tracer_parcours(val)

    @property
    def get_distance(self) -> float:
        """ Retourne la distance du robot et obstacle
        :return: la distance du robot
        """
        return self.simulation.detecte_distance(self.robot)
