import math

from ..controller.controleur import Adaptateur
from ..robot.robot2I013 import Robot2IN013


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