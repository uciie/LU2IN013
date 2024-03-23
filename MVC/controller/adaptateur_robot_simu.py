from MVC.controller.controleur import Adaptateur
from MVC.modele.objets import SimuRobot
from MVC.modele.simulation import Simulation
from MVC.modele.vecteur import Vecteur


class AdaptateurRobotSimu(Adaptateur):
    def __init__(self, robot: SimuRobot, simulation: Simulation):
        """
        """
        super().__init__()
        self._robot = robot
        self._simulation = simulation

        self._last_theta = self._robot.last_theta
        self._last_pos_x, self._last_pos_y = self._robot.last_pos_x, self._robot.last_pos_y

    @property
    def last_theta(self):
        return self._last_theta

    @last_theta.setter
    def last_theta(self, theta: float):
        self._last_theta = theta

    @property
    def last_pos_x(self):
        return self._last_pos_x

    @last_pos_x.setter
    def last_pos_x(self, x: float):
        self._last_pos_x = x

    @property
    def last_pos_y(self):
        return self._last_pos_y

    @last_pos_y.setter
    def last_pos_y(self, y: float):
        self._last_pos_y = y

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
        distance = Vecteur(self._robot.pos_x - self._last_pos_x, self._robot.pos_y - self._last_pos_y)
        self._last_pos_x, self._last_pos_y = self._robot.pos_x, self._robot.pos_y
        return distance.norme

    @property
    def angle_parcourue(self) -> float:
        """ Obtenir l'angle parcouru
        :return: l'angle parcouru
        """
        angle = self._robot.theta - self._last_theta
        self._last_theta = self._robot.theta
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
        # self._simulation.update()
        pass
