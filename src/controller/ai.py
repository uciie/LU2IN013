import logging
import math
import cv2
from PIL import Image
from ..controller.controleur import Adaptateur, Strategie

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

# Désactiver les messages de journalisation pour le module spécifié
# logging.getLogger('src.controller.ai').setLevel(logging.WARNING)

class Go(Strategie):
    """ Classe responsable d'avancer le robot """

    def __init__(self, adaptateur: Adaptateur, distance: float, v_ang_d: float, v_ang_g: float,
                 active_trace: bool = False) -> None:
        """
        :param adaptateur: l'adaptateur du robot
        :param distance: la distance à parcourir robot
        :param v_ang_d: la vitesse angulaire droite du robot
        :param v_ang_g: la vitesse angulaire gauche du robot
        :param active_trace: activation du tracage du parcours du robot
        """
        super().__init__()
        self.adaptateur = adaptateur
        self.pos_ini = None
        self.distance = distance
        self.v_ang_d, self.v_ang_g = v_ang_d, v_ang_g
        self.parcouru = 0.
        self.active_trace = active_trace
        self.logger = logging.getLogger(__name__)

    def start(self):
        """Commencer la strategie"""
        self.logger.info("Starting Go strategy")
        self.adaptateur.active_trace(self.active_trace)
        self.adaptateur.set_vitesse_roue(self.v_ang_d, self.v_ang_g)
        self.pos_ini = self.adaptateur.distance_et_angle_parcourus()[0]
        self.parcouru = 0.

    def stop(self):
        """Verifier si la strategie est fini ou non
        :return: True si la strategie est finie, False sinon"""
        self.logger.info(f"distance parcourue {self.parcouru}, distance {self.distance}")
        # v_roue_d, v_roue_g = self.adaptateur.vitesse_ang_roues
        return math.fabs(self.parcouru) >= math.fabs(self.distance) #or self.adaptateur.get_distance() < self.condition

    def step(self):
        """pas de la strategie """
        self.parcouru += self.adaptateur.distance_et_angle_parcourus()[0]
        if self.stop():
            self.adaptateur.stop()
            self.logger.info("Go strategy finished")
            return


class TournerDeg(Strategie):
    """Classe qui permet de tourner le robot d'un certain degree"""

    def __init__(self, adaptateur: Adaptateur, angle: float, v_ang: float, active_trace: bool = False) -> None:
        """
        :param adaptateur: l'adaptateur du robot
        :param angle: l'angle à parcourir robot
        :param v_ang: la vitesse angulaire du robot
        :param active_trace: activation du tracage du parcours du robot
        """
        super().__init__()
        self.pos_ini = None
        self.adaptateur = adaptateur
        self.angle, self.v_ang = angle, v_ang
        self.parcouru = 0.
        self.active_trace = active_trace
        self.logger = logging.getLogger(__name__)

    def start(self):
        """Commencer la strategie"""
        self.logger.info("Starting TournerDeg strategy")
        #self.logger.info(f"adapateur angle {self.adaptateur.angle}")
        self.adaptateur.active_trace(self.active_trace)
        if self.angle is None : 
            if self.adaptateur.angle < 90:
                self.angle = 90 - self.adaptateur.angle
            else : 
                self.angle = self.adaptateur.angle-90
        if self.angle > 0:
            self.v_ang_d, self.v_ang_g = self.v_ang, -self.v_ang
            self.adaptateur.set_vitesse_roue(self.v_ang, -self.v_ang)
        else:
            self.v_ang_d, self.v_ang_g = -self.v_ang, self.v_ang
            self.adaptateur.set_vitesse_roue(-self.v_ang, self.v_ang)
        self.pos_ini = 1. * self.adaptateur.distance_et_angle_parcourus()[1]
        self.parcouru = 0

    def stop(self) -> bool:
        """Verifier si la strategie est fini ou non
        :return: True si la strategie est finie ou False sinon"""
        self.logger.info(f"angle parcourue {self.parcouru}, angle {self.angle}")
        if self.angle == 0 or math.fabs(self.parcouru) >= math.fabs(self.angle):
            self.adaptateur.stop()
            return True
        return False

    def step(self):
        """pas de la strategie"""
        self.parcouru += self.adaptateur.distance_et_angle_parcourus()[1]
        if self.stop():
            self.logger.info("TournerDeg strategy finished")
            return


class StrategieSequentielle(Strategie):
    """Classe Strategie sequentielle permettant de faire des combinaisons de la strategie basique"""

    def __init__(self, adaptateur: Adaptateur, steps: list[Strategie]) -> None:
        """
        :param adaptateur: adaptateur du robot
        :param steps: liste des steps
        """
        super().__init__()
        self.adaptateur = adaptateur
        self.pos_ini = None
        self.parcouru = 0.
        self.steps = steps
        self.current_step = 0

        self.logger = logging.getLogger(__name__)

    def start(self):
        """commencer la strategie"""
        self.logger.info("Starting Sequential strategy")
        self.current_step = 0
        self.steps[self.current_step].start()

    def stop(self) -> bool:
        """Verifier si la strategie est finie
        :return: True si la strategie est finie, False sinon"""
        return self.current_step >= len(self.steps) or self.steps[self.current_step].stop()

    def step(self):
        """pas de la strategie sequentielle """
        if self.stop():
            return
        self.steps[self.current_step].step()
        if self.steps[self.current_step].stop():
            self.current_step += 1
            if self.current_step < len(self.steps):
                self.steps[self.current_step].start()


class Stop(Strategie):
    """Strategie qui ne fait rien/ arrete le robot"""

    def __init__(self, adaptateur: Adaptateur):
        """
        :param adaptateur: adaptateur du robot
        """
        super().__init__()
        self.adaptateur = adaptateur
        self.logger = logging.getLogger(__name__)

    def start(self):
        """commencer la strategie"""
        self.logger.info("Starting STOP strategy")
        self.adaptateur.set_vitesse_roue(0, 0)

    def stop(self) -> bool:
        """Verifier si la strategie est finie
        :return: True si la strategie est finie, False sinon"""
        return True

    def step(self):
        pass


class StrategieIf(Strategie):
    """Classe Strategie conditionnelle faire strat_a si condition verifiée, sinon strat_b"""

    def __init__(self, adaptateur: Adaptateur, strat_a: Strategie, strat_b: Strategie, condition: float) -> None:
        """
        :param adaptateur: adaptateur du robot
        :param strat_a: strategie A
        :param strat_b: strategie B
        :param condition: condition
        """
        super().__init__()
        self.adaptateur = adaptateur
        self.stratA = strat_a
        self.stratB = strat_b

        self.condition = condition
        self.current_step = 0
        self.logger = logging.getLogger(__name__)

        # Initialise strat_a_faire à None
        self.strat_a_faire = None

    def start(self):
        """commencer la strategie"""
        self.logger.info("Starting condition strategy")
        #self.logger.info(f"capteur distance {self.adaptateur.get_distance()}")
        if self.adaptateur.get_distance() >= self.condition:
            self.strat_a_faire = self.stratA
        else:
            self.strat_a_faire = self.stratB
        self.strat_a_faire.start()

    def stop(self) -> bool:
        """Verifier si la strategie est finie
        :return: True si la strategie est finie, False sinon"""
        # Verifier si strat_a_faire n'est pas vide
        if self.strat_a_faire is not None:
            return self.strat_a_faire.stop()

    def step(self):
        """pas de la strategie sequentielle """
        if self.strat_a_faire is not None:
            self.strat_a_faire.step()


class StrategieWhile(Strategie):
    """Classe Strategie while: faire strategie tant que condition verifiée"""

    def __init__(self, adaptateur: Adaptateur, strat: Strategie, condition: float) -> None:
        """
        :param adaptateur: adaptateur du robot
        :param strat: strategie
        :param condition: condition
        """
        super().__init__()
        self.adaptateur = adaptateur
        self.strat = strat

        self.condition = condition
        self.logger = logging.getLogger(__name__)

    def start(self):
        """commencer la strategie"""
        self.logger.info("Starting while strategy")
        self.strat.start()

    def stop(self) -> bool:
        """Verifier si la strategie est finie
        :return: True si la strategie est finie, False sinon"""
        self.logger.info(f"capteur distance :  {self.adaptateur.get_distance()}, condition :{self.condition}")
        if self.adaptateur.get_distance() < self.condition : 
            self.logger.info(f"STOP !!! ")
            self.adaptateur.stop()
            return True
        else : 
            if self.strat.stop():
                self.strat.start()
                return False

    def step(self):
        """pas de la strategie sequentielle """
        if self.stop():
            return 
        self.strat.step()

class StrategieTrouverBalise(Strategie):
    """Classe Strategie pour trouver une balise"""
    def __init__(self, adaptateur: Adaptateur, angle: int =20, pas_angle: int=10, seuil_cpt:int = 15) -> None:
        """
        :param adaptateur: adaptateur du robot
        :param angle: angle de rotation au depart
        :param pas_angle: pas de rotation du servo moteur
        :param seuil_cpt: seuil du nb de capture d'image
        :param vitesse: vitesse du robot
        """
        super().__init__()
        self.adaptateur = adaptateur
        self.angle = angle
        self.pas_angle = pas_angle # Pas de rotation du servo moteur
        self.cpt = 0
        self.image = None
        self.seuil_cpt = seuil_cpt # Seuil du nb de capture d'image
        self.logger = logging.getLogger(__name__)

    def start(self):
        """Commencer la strategie"""
        self.logger.info("Starting StrategieTrouverBalise strategy")
        self.adaptateur.start_recording()
        self.adaptateur.servo_rotate(self.angle)

    def stop(self) -> bool:
        """Vérifier si la stratégie est finie
        :return: True si la stratégie est finie, False sinon"""
        if self._process_image():
            self.logger.info(f"Balise trouvée: {self.num}")
            return True
        self.logger.info(self.cpt)
        return self.cpt > self.seuil_cpt
    
    def step(self):
        """Pas de la stratégie"""
        if self.stop():
            self.adaptateur.stop_recording()
            return
        self.image = self.adaptateur.get_image()
        if self.image is not None: 
            self.angle += self.pas_angle
            self.adaptateur.servo_rotate(self.angle)
            self.cpt += 1

    def _process_image(self) -> bool:
        """Traite l'image capturée pour vérifier la présence de la balise
        :return: True si la balise est trouvée, False sinon"""
        if self.image is not None:
            image_path = f"image{self.cpt}.png"
            im = Image.fromarray(self.image)
            im.save(image_path)
            image_charge = cv2.imread(image_path)
            res, self.num = self.adaptateur.reconnaissance_im(image_charge, self.cpt)
            return res
        else:
            self.logger.info("Aucune image n'a été capturée.")
        return False