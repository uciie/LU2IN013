import threading
import time
from abc import ABC, abstractmethod
from threading import Thread


class Adaptateur(ABC):
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

    @property
    @abstractmethod
    def vitesse_ang_roues(self) -> tuple[float, float]:
        """ Obtenir la vitesse angulaire des roues
        """
        pass

    @property
    @abstractmethod
    def distance_parcourue(self) -> float:
        """ Obtenir la distance parcourue
        """
        pass

    @property
    @abstractmethod
    def angle_parcourue(self) -> float:
        """ Obtenir l'angle parcouru
        """
        pass

    @property
    @abstractmethod
    def stop(self):
        """ Arreter le robot
        """
        pass

    @property
    @abstractmethod
    def robot(self):
        """
        """
        pass

    @abstractmethod
    def actualiser(self):
        """Actualiser la simulation
        """
        pass


class Strategie(ABC):
    def __init__(self):  # , adaptateur: Adaptateur):
        """ Initialise la classe Strategie
        """
        # self._adaptateur = adaptateur

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self) -> bool:
        pass

    @abstractmethod
    def step(self):
        pass


class Controleur(Thread):
    def __init__(self, adaptateur: Adaptateur, dt: float, lock: threading.RLock):
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

        # liste strat
        self.liste_strat = []

        self.cur = -1
        # Le dt
        self.dt = dt
        self.lock = lock
        self._running = False

    def add_strat(self, strat: Strategie):
        """ Ajouter une strategie au conntroleur

        :param strat: Une strategie
        """
        self.liste_strat.append(strat)

    def stop(self):
        """Vérifie si toutes les étapes sont terminées
        """
        if not self.liste_strat:
            return True
        return self.cur == len(self.liste_strat) - 1 and self.liste_strat[self.cur].stop()

    def run(self):

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
        if self.cur < 0 or self.liste_strat[self.cur].stop():
            self.cur += 1
            self.liste_strat[self.cur].start()
        self.liste_strat[self.cur].step()
