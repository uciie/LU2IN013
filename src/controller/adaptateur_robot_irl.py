import math
import logging
import cv2
import numpy as np
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
    

# plage de couleurs pour la reconnaissance d'image (balise)
plages_couleurs = {
    'jaune': {
        'lower': np.array([90, 90, 30]),  # foncé
        'upper': np.array([220, 200, 100])  # clair
    },
    'rouge': {
        'lower': np.array([90, 0, 10]),
        'upper': np.array([210, 80, 80])
    },
    'bleu': {
        'lower': np.array([0, 10, 100]),
        'upper': np.array([20, 80, 170])
    },
    'vert': {
        'lower': np.array([0, 40, 50]),
        'upper': np.array([70, 150, 140])
    }
}

def masque_couleur(image):
    """Trouver les contours des couleurs dans l'image
    :param image: Image à traiter
    :return: Dictionnaire des contours pour chaque couleur"""
    # Convertir l'image en RVB
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Créer un masque pour chaque couleur dans l'image
    masks = {}
    for color, values in plages_couleurs.items():
        masks[color] = cv2.inRange(rgb, values['lower'], values['upper'])

    # Trouver les contours pour chaque couleur
    contours = {}
    for color, mask in masks.items():
        contours[color], _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return contours, image    

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

    def distance_parcourue(self) -> float:
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

        return distance_parcourue

    def angle_parcouru(self) -> float:
        """ Obtenir l'angle parcouru
        :returns : Renvoie l'angle parcourut du robot en degree
        """
        current_motor_positions = self._robot.get_motor_position()
        # Calcul de la différence entre les positions des moteurs gauche et droit
        delta_left_motor = (current_motor_positions[0] - self._last_motor_positions[0])
        delta_right_motor = (current_motor_positions[1] - self._last_motor_positions[1])
        angle_cur = math.fabs(self._robot.WHEEL_DIAMETER * (
                    -delta_left_motor + delta_right_motor) / (2 * self._robot.WHEEL_BASE_WIDTH))
        
        self.logger.info(f"angle parcouru left: {delta_left_motor}, angle parcouru right: {delta_right_motor}")
        self._last_motor_positions = current_motor_positions

        return angle_cur

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
    
    def servo_rotate(self, angle: int):
        """
        Fait tourner le servo moteur
        :param angle: Angle de rotation du servo moteur
        """
        self._robot.servo_rotate(angle)
        self._angle = angle
    
    def reconnaissance_im(self, image, num)->tuple[bool, int]:
        """Reconnaissance d'image balise 
        :param image: Image à traiter
        :param num: numero de l'image
        :return: Tuple (bool, int) : (True, num) si la reconnaissance est un succès, sinon (False, -1)
        """
        self.logger.info("Reconnaissance d'image")
        contours, resized = masque_couleur(image)

        # Filtrer les contours pour ne garder que ceux qui ressemblent à un rectangle
        rectangles = {}
        dico_rectangles = dict()
        for color, color_contours in contours.items():
            rectangles[color] = []
            for contour in color_contours:
                # Approximer le contour pour un polygone
                epsilon = 0.1 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                # Si le polygone a 4 côtés, il est probablement un rectangle
                if len(approx) == 4:
                    self.logger.info(f"Rectangle {color}")
                    dico_rectangles[color] = approx
                    rectangles[color].append(approx)

        # Vérifier si les clés de dico_rectangles sont bien les couleurs (rouge, vert, jaune, bleu)
        expected_colors = ['rouge', 'vert', 'jaune', 'bleu']
        if set(dico_rectangles.keys()) == set(expected_colors):
            # Calculer les coordonnées du rectangle englobant
            min_x = min([rect[0][0][0] for rect in dico_rectangles.values()])
            max_x = max([rect[2][0][0] for rect in dico_rectangles.values()])
            min_y = min([rect[0][0][1] for rect in dico_rectangles.values()])
            max_y = max([rect[2][0][1] for rect in dico_rectangles.values()])

            # Dessiner les rectangles sur l'image originale
            #for color, rect in dico_rectangles.items():
            #    cv2.drawContours(image, [rect], -1, (0, 255, 0), 2)  # Dessiner le rectangle vert

            # Vérifier si le rectangle englobant est un rectangle
            width = max_x - min_x
            height = max_y - min_y
            if width > 0 and height > 0:
                self.logger.info("Le rectangle englobant est un rectangle.")
                # Dessiner le rectangle englobant
                # cv2.rectangle(image, (min_x, min_y), (max_x, max_y), (255, 0, 0), 2)
                return True, num
            else:
                self.logger.info("Le rectangle englobant n'est pas un rectangle.")
                return False, -1
        else:
            return False, -1