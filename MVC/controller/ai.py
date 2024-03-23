import logging
import math

from ..controller.controleur import Adaptateur, Strategie

# Configure logging
logging.basicConfig(level=logging.DEBUG, filename='ai.log', filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# Désactiver les messages de journalisation pour le module spécifié
# logging.getLogger('MVC.controller.ai').setLevel(logging.WARNING)

class Go(Strategie):
    def __init__(self, adaptateur: Adaptateur, distance: float, v_ang_d: float, v_ang_g: float,
                 active_trace: bool) -> None:
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
        self.logger.info("Starting Go strategy")
        self.adaptateur.active_trace(self.active_trace)
        self.adaptateur.set_vitesse_roue(self.v_ang_d, self.v_ang_g)
        self.pos_ini = self.adaptateur.distance_parcourue
        self.parcouru = 0.

    def stop(self):
        """Verifier si la strategie est fini ou non"""
        self.logger.info(f"distance parcourue {self.parcouru}, distance {self.distance}")
        # v_roue_d, v_roue_g = self.adaptateur.vitesse_ang_roues
        return math.fabs(self.parcouru) >= math.fabs(self.distance)

    def step(self):
        self.parcouru += self.adaptateur.distance_parcourue
        if self.stop():
            self.adaptateur.stop()
            self.logger.info("Go strategy finished")
            return


class TournerDeg(Strategie):
    def __init__(self, adaptateur: Adaptateur, angle: float, v_ang: float, active_trace: bool) -> None:
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
        self.logger.info("Starting TournerDeg strategy")
        self.adaptateur.active_trace(self.active_trace)
        if self.angle > 0:
            self.v_ang_d, self.v_ang_g = self.v_ang, -self.v_ang
            self.adaptateur.set_vitesse_roue(self.v_ang, -self.v_ang)
        else:
            self.v_ang_d, self.v_ang_g = -self.v_ang, self.v_ang
            self.adaptateur.set_vitesse_roue(-self.v_ang, self.v_ang)
        self.pos_ini = 1. * self.adaptateur.angle_parcourue
        self.parcouru = 0.

    def stop(self) -> bool:
        """Verifier si la strategie est fini ou non"""
        self.logger.info(f"angle parcourue {self.parcouru}, angle {self.angle}")
        return math.fabs(self.parcouru) >= math.fabs(self.angle)

    def step(self):
        self.parcouru += self.adaptateur.angle_parcourue
        if self.stop():
            self.adaptateur.stop()
            self.logger.info("TournerDeg strategy finished")
            return


class StrategieSequentielle(Strategie):
    def __init__(self, adaptateur: Adaptateur, steps: list[Strategie], active_trace: bool) -> None:
        """
        :param adaptateur: adaptateur du robot
        :param steps: liste des steps
        :param active_trace: True si on veut la tracage du parcours, sinon false
        """
        super().__init__()
        self.adaptateur = adaptateur
        self.pos_ini = None
        self.parcouru = 0.
        self.steps = steps
        self.current_step = 0
        self.active_trace = active_trace

        self.logger = logging.getLogger(__name__)

    def start(self):
        """commencer la strategie"""
        self.logger.info("Starting Sequential strategy")
        self.current_step = 0
        self.steps[self.current_step].start()

    def stop(self) -> bool:
        """Verifier si la strategie est finie"""
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
