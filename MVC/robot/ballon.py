import math
import threading
import math
from abc import ABC, abstractmethod

from .vecteur import Vecteur
from .modele import objets
from ..robot.accessoirs import Capteur

class ballon:
    """ exo 2 """

    def __init__(self, name: str, pos_x: float, pos_y: float, dim_length: float, dim_width: float, color: str):
        """Initialisation du ballon """
        self.name = name

        # Initialisation de la position du robot
        self._pos_x = pos_x
        self._pos_y = pos_y

        # Dimension du ballon sur la fenêtre
        self.length = dim_length  
        self.width = dim_width  

        #couleur du ballon 
        self.color = color

        self.vectDir = Vecteur(0, -1)

        # Activation du tracage du parcours
        self._tracer_parcours = None

        # Capteur du ballon
        self.capteur = Capteur(Vecteur(self.vectDir.x, int(self.vectDir.y / abs(self.vectDir.y))))

        
        
