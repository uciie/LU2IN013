import threading
import time
from abc import ABC, abstractmethod
from threading import Thread


class Adaptateur(ABC):
    """Classe mere d'adaptateur de robot'"""

    def __init__(self) -> None:
        """ Initialise l'adaptateur
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
        """ Mettre à jour la vitesse angulaire de la route droite"""
        self._v_ang_roue_d = value

    @property
    def v_ang_g(self) -> float:
        """ Obtenir la vitesse angulaire de la route droite
        """
        return self._v_ang_roue_g

    @v_ang_g.setter
    def v_ang_g(self, value: float):
        """ Mettre à jour la vitesse angulaire de la route gauche"""
        self._v_ang_roue_g = value

    @abstractmethod
    def set_vitesse_roue(self, v_ang_roue_d: float, v_ang_roue_g: float):
        """ Modifier la vitesse des roues
        """
        pass

    @abstractmethod
    def distance_parcourue(self) -> float:
        """ Obtenir la distance parcourue
        """
        pass

    @abstractmethod
    def angle_parcouru(self) -> float:
        """ Obtenir l'angle parcouru
        """
        pass

    @property
    @abstractmethod
    def stop(self):
        """ Arreter le robot
        """
        pass

    @abstractmethod
    def active_trace(self, val: bool):
        """ Activation du tracage de parcours"""
        pass

    @abstractmethod
    def get_distance(self) -> float:
        """La distance du robot et l'obstacle"""
        pass

    @abstractmethod
    def rayon(self) -> float:
        """Rayon de rotation"""
        pass


class Strategie(ABC):
    """Classe mere de strategie"""

    def __init__(self):  # , adaptateur: Adaptateur):
        """ Initialise la classe Strategie
        """
        # self._adaptateur = adaptateur

    @abstractmethod
    def start(self):
        """Commencer strategie"""
        pass

    @abstractmethod
    def stop(self) -> bool:
        """Verifier si strategie est finie"""
        pass

    @abstractmethod
    def step(self):
        """pas de la strategie """
        pass


class Controleur(Thread):
    """classe Controleur"""

    def __init__(self, adaptateur: Adaptateur, dt: float):
        """
        Initialise le contrôleur avec un robot, une vue et un intervalle de temps.

        :param adaptateur: Le robot
        :param dt: Le dt
        """
        super(Controleur, self).__init__()
        # Modèle
        self.adaptateur = adaptateur

        # Vues
        self.view = None

        # Le dt
        self.dt = dt
        # self.lock = lock
        self._running = False
        self.strat = None

    def add_strat(self, strat: Strategie):
        """ Ajouter une strategie au conntroleur

        :param strat: Une strategie
        """
        self.strat = strat
        self.strat.start()

    def stop(self) -> bool:
        """Vérifie si toutes les étapes sont terminées
        """
        if not self.strat:
            return True
        return self.strat.stop()

    def run(self):
        """Activer le controleur"""
        self._running = True
        while self._running:
            self.step()
            time.sleep(self.dt)

    def step(self):
        """Faire la commande suivante"""
        # with self.lock:
        if self.stop():
            return
        # Faire la stratégie suivante
        self.strat.step()
