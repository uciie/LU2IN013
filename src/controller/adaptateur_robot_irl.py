import math
import logging
from src.controller.controleur import Adaptateur
# Configure logging to write to both terminal and file
logging.basicConfig(level=logging.DEBUG, filename='logs/simu.log', filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Créer un gestionnaire pour afficher les messages dans le terminal
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Définir le niveau de logging pour la sortie terminal
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Récupérer le logger racine
root_logger = logging.getLogger()
root_logger.addHandler(console_handler)

try :
    from robot2IN013 import Robot2IN013
except ModuleNotFoundError:
    from src.robot.robot2I013Fake import Robot2IN013


class AdaptateurRobotIrl(Adaptateur):
    """Classe de l'adaptateur du robot irl"""

    def __init__(self, robot: Robot2IN013):
        """ Adaptateur du robot irl
        """
        super().__init__()
        self._robot = robot
        self._v_ang_roue_d, self._v_ang_roue_g = 0., 0.
        self._last_motor_positions = self._robot.get_motor_position()
        self.logger = logging.getLogger(__name__)
        self._angle = 0
        self.servo_rotate(0) # initialiser l'angle du servo moteur

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
        return self._robot.WHEEL_BASE_WIDTH/2

    def distance_et_angle_parcourus(self) -> float:
        """ Obtenir la distance parcourue en mm 
        :returns : Renvoie la distance parcourue du robot
        """
        current_motor_positions = self._robot.get_motor_position()

        # Calcul de la distance parcourue par chaque roue
        distance_left_wheel = math.fabs((current_motor_positions[0] - self._last_motor_positions[0]) * self._robot.WHEEL_DIAMETER*math.pi) /360
        distance_right_wheel = math.fabs((current_motor_positions[1] - self._last_motor_positions[1]) * self._robot.WHEEL_DIAMETER*math.pi)/360

        # Calcul de la distance totale parcourue (moyenne des deux distances)
        distance_parcourue = (distance_left_wheel + distance_right_wheel) / 2

        # Mise à jour de la dernière position des moteurs
        self._last_motor_positions = current_motor_positions

        # Calcul de la différence entre les positions des moteurs gauche et droit
        delta_left_motor = (current_motor_positions[0] - self._last_motor_positions[0])
        delta_right_motor = (current_motor_positions[1] - self._last_motor_positions[1])
        angle_cur = math.fabs(self._robot.WHEEL_DIAMETER * (
                    -delta_left_motor + delta_right_motor) / (2 * self._robot.WHEEL_BASE_WIDTH))
        
        self.logger.info(f"angle parcouru left: {delta_left_motor}, angle parcouru right: {delta_right_motor}")
        self._last_motor_positions = current_motor_positions

        return distance_parcourue, angle_cur

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

    def get_distance(self) -> float:
        """
        Lit le capteur de distance (en mm)
        """
        distance = self._robot.get_distance()
        self.logger.info(f"capteur distance: {distance}")
        return distance
    
    @property
    def angle(self)->int:
        """"""
        return self._angle
    
    def start_recording(self):
        """
        Démarre l'enregistrement des images
        """
        self._robot.start_recording()

    def stop_recording(self):
        """
        Arrête l'enregistrement des images
        """
        self._robot.stop_recording()

    def get_image(self):
        """
        Capture la derniere image avec la caméra du robot
        :return: Image capturée par la caméra du robot
        """
        return self._robot.get_image()
    
    def servo_rotate(self, angle: int):
        """
        Fait tourner le servo moteur
        :param angle: Angle de rotation du servo moteur
        """
        self._robot.servo_rotate(angle)
        self._angle = angle
    