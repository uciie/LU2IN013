import math

from src.controller.controleur import Adaptateur
from src.robot.robot2I013 import Robot2IN013


class AdaptateurRobotIrl(Adaptateur):
    """Classe de l'adaptateur du robot irl"""

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

    def set_vitesse_roue(self, v_ang_roue_d: float, v_ang_roue_g: float):
        """ Modifier la vitesse des roues

        :param v_ang_roue_d: Modifier la vitesse angulaire de la roue droite
        :param v_ang_roue_g: Modifier la vitesse angulaire de la roue gauche
        """
        self._v_ang_roue_d = v_ang_roue_d
        self._v_ang_roue_g = v_ang_roue_g
        self._robot.set_motor_dps(self._robot.MOTOR_RIGHT, v_ang_roue_d)  # port : 1
        self._robot.set_motor_dps(self._robot.MOTOR_LEFT, v_ang_roue_g)  # port : 2

    @property
    def rayon(self) -> float:
        """ Rayon de rotation du robot"""
        return self._robot.WHEEL_BASE_WIDTH

    def distance_parcourue(self) -> float:
        """ Obtenir la distance parcourue
        :returns : Renvoie la distance parcourue du robot
        """
        return self.angle_parcourue / 360 * self._robot.WHEEL_DIAMETER * math.pi

    @property
    def angle_parcourue(self) -> float:
        """ Obtenir l'angle parcouru
        :returns : Renvoie l'angle parcourut du robot en degree
        """
        # obtenir la position des angles des roues
        pos_roues_x, pos_roues_y = self._robot.get_motor_position()
        # moyenne d'angle parcourue
        angle = (pos_roues_x + pos_roues_y) / 2

        self._robot.offset_motor_encoder(self._robot.MOTOR_LEFT, self._robot.read_encoders()[0])
        self._robot.offset_motor_encoder(self._robot.MOTOR_RIGHT, self._robot.read_encoders()[1])

        return angle

    def stop(self):
        """ Arreter le robot irl
        """
        self.set_vitesse_roue(0, 0)

    @property
    def info(self) -> str:
        """ afficher les informations du robot
        :return str: informations du robot
        """
        info_str = ""
        info_str += f"Vitesse roue droite: {self._v_ang_roue_d}\n"
        info_str += f"Vitesse roue gauche: {self._v_ang_roue_g}\n"
        return info_str

    def active_trace(self, val: bool):
        pass

    @property
    def get_distance(self) -> float:
        """
        Lit le capteur de distance (en mm).
        :returns: Entier distance en millimetre.
            1. L'intervalle est de **5-8,000** millimeters.
            2. Lorsque la valeur est en dehors de l'intervalle, le retour est **8190**.
        """
        return self._robot.get_distance()
