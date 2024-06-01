import threading
import time
from abc import ABC, abstractmethod
from threading import Thread
import cv2
import numpy as np

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

class Adaptateur(ABC):
    """Classe mere d'adaptateur de robot'"""

    def __init__(self) -> None:
        """ Initialise l'adaptateur
        """
        self._v_ang_roue_d = 0
        self._v_ang_roue_g = 0

    @abstractmethod
    def set_vitesse_roue(self, v_ang_roue_d: float, v_ang_roue_g: float):
        """ Modifier la vitesse des roues
        """
        pass

    @abstractmethod
    def distance_et_angle_parcourus(self) -> tuple[float, float]:
        """ Obtenir la distance  et l'angle parcourus
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

    @abstractmethod
    def get_image(self):
        """Obtenir l'image du robot"""
        pass

    @abstractmethod
    def servo_rotate(self, angle: int):
        """Faire tourner le servo moteur"""
        pass

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

            # Vérifier si le rectangle englobant est un rectangle
            width = max_x - min_x
            height = max_y - min_y
            if width > 0 and height > 0:
                self.logger.info("Le rectangle englobant est un rectangle.")
                return True, num
            else:
                self.logger.info("Le rectangle englobant n'est pas un rectangle.")
                return False, -1
        else:
            return False, -1

class Strategie(ABC):
    """Classe mere de strategie"""

    def __init__(self):
        """ Initialise la classe Strategie
        """

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
        if self.stop():
            return
        # Faire la stratégie suivante
        self.strat.step()
