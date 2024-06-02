import logging
from src.controller.controleur import Adaptateur
from src.modele.objets import SimuRobot
from src.modele.simulation import Simulation
from src.modele.utilitaire import distance, point_le_plus_loin, check_directory

# Configure logging
logging.basicConfig(level=logging.DEBUG, filename='logs/simu.log', filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# Désactiver les messages de journalisation pour le module spécifié
# logging.getLogger('src.controller.ai').setLevel(logging.WARNING)

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
        self._affichage3d = None
        self._last_theta = self._robot.last_theta
        self._last_pos_x, self._last_pos_y = self._robot.last_pos_x, self._robot.last_pos_y
        self.logger = logging.getLogger(__name__)

    @property
    def rayon(self) -> float:
        """Rayon de rotation"""
        point_loin = point_le_plus_loin(self._robot.coins, self._robot.pos_x, self._robot.pos_y)
        return distance((self._robot.pos_x, self._robot.pos_y), point_loin)

    @property
    def last_theta(self) -> float:
        """Getter dernier tetha enregistre depuis le dernier appel
        :return float: l'angle theta du robot'"""
        return self._last_theta

    @last_theta.setter
    def last_theta(self, theta: float):
        """Setter du dernier angle theta enregistre depuis le dernier appel
        :param float theta: nouvel angle theta '"""
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

    def set_affichage3d(self, affichage3d):
        """Setter de l'affichage 3d
        :param affichage3d: l'affichage 3d"""
        self._affichage3d = affichage3d

    def set_vitesse_roue(self, v_ang_roue_d: float, v_ang_roue_g: float):
        """ Modifier la vitesse des roues

        :param v_ang_roue_d: Modifier la vitesse angulaire de la roue droite
        :param v_ang_roue_g: Modifier la vitesse angulaire de la roue gauche
        """
        self._robot.roue_droite.vitesse_angulaire = v_ang_roue_d
        self._robot.roue_gauche.vitesse_angulaire = v_ang_roue_g

    def distance_et_angle_parcourus(self) -> tuple[float, float]:
        """ Obtenir la distance et l'angle parcourus
        :return: un tuple contenant la distance parcourue et l'angle parcouru
        """
        # Calcul de la distance parcourue
        dist = distance((self._robot.pos_x, self._robot.pos_y), (self._last_pos_x, self._last_pos_y))
        self._last_pos_x, self._last_pos_y = self._robot.pos_x, self._robot.pos_y

        # Calcul de l'angle parcouru
        angle = self._robot.theta - self._last_theta
        # Ajustement de l'angle parcouru selon le sens trigonométrique ou horloge
        if angle < -180:
            angle += 360
        elif angle > 180:
            angle -= 360
        self._last_theta = self._robot.theta

        return dist, angle

    def stop(self):
        """ Arreter le robot irl
        :return: True si le robot est en arret
        """
        self.set_vitesse_roue(0, 0)

    def active_trace(self, val: bool):
        """Activer ou désactiver le tracage du robot.
        :param val: True pour activer le tracage, False pour le désactiver"""
        self._robot.activer_tracer_parcours(val)

    def get_distance(self) -> float:
        """ Retourne la distance du robot et obstacle
        :return: la distance du robot
        """
        return self._simulation.detecte_distance(self._robot)
    
    def start_recording(self):
        """Commencer l'enregistrement"""
        check_directory()
        self._affichage3d.recording = True

    def stop_recording(self):
        """
        Arrête l'enregistrement des images
        """
        self._affichage3d.recording = False

    def get_image(self):
        """Obtenir l'image du robot"""
        return self._affichage3d.image
    
    def servo_rotate(self, angle: int):
        """Faire tourner le servo moteur"""
        self._affichage3d.camera.setH(angle)