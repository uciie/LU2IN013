# @authors Équipe HELMS
from .vecteur import Vecteur

import math
# Supposons que les robots sont en forme de rectangle/carré
# Supposons que la position du robot (x, y) correspond à l'extrémité en haut à gauche

class Roue:
    def __init__(self, rayon: float, vmax_ang: float):
        """Initialisation d'une roue

        :param rayon: Le rayon de la roue
        :param vmax_ang: La vitesse angulaire maximale de la roue
        """
        self._rayon = rayon  # m
        self._vmax_ang = vmax_ang  # rad/s
        self._vitesse_angulaire = 0.0  # rad/s

    @property
    def rayon(self) -> float:
        """Obtient le rayon de la roue."""
        return self._rayon

    @property
    def vmax_ang(self) -> float:
        """Obtient la vitesse angulaire maximale de la roue."""
        return self._vmax_ang

    @property
    def vitesse_angulaire(self) -> float:
        """Obtient la vitesse angulaire actuelle de la roue."""
        return self._vitesse_angulaire

    @vitesse_angulaire.setter
    def vitesse_angulaire(self, value: float) -> None:
        """Modifie la vitesse angulaire de la roue, en s'assurant qu'elle ne dépasse pas la vitesse maximale.

        :param value: Nouvelle vitesse angulaire de la roue.
        """
        self._vitesse_angulaire = min(value, self._vmax_ang)


class Robot:
    def __init__(self, name: str, posX: float, posY: float, dimLength: float, dimWidth: float, rayon_roue:int , vmax_ang : float, color: str):
        """Initialisation du robot.

        :param name: Nom du robot (str).
        :param posX: Coordonnée x du robot (float).
        :param posY: Coordonnée y du robot (float).
        :param dimLength: Longueur de la pièce en mètres (float).
        :param dimWidth: Largeur de la pièce en mètres (float).
        :paarm capteur : Capteur de distance du robot 
        :param vectDir: Vecteur directeur du robot (Vecteur).
        :param rayon_roue: Rayon des roues du robot (int)
        :param vmax_ang : Vitesse maximale angulaire du robot 
        :param color: Couleur du robot (str).
        :returns: Retourne une instance de la classe Robot.
        """
        # Nom du robot
        self.name = name

        # Fenêtre graphique
        # Identifiants des objets graphiques dans l'interface
        self.rect_id = None  # Identifiant du rectangle
        self.arrow_id = None  # Identifiant de la flèche
        self.line_id = None  # Identifiant de sa tracabilite
        self.color = color  # couleur du robot

        self.vectDir = Vecteur(0,-1) #vectDir

        # Dimension du robot sur la fenêtre
        self.length = dimLength  # /self.grille.echelle
        self.width = dimWidth  # /self.grille.echelle

        #Initisalisation de la position du robot
        self.posX = posX
        self.posY = posY

        # Ancienne position du robot
        # Initialise l'ancienne position à la position actuelle
        self.lastPosX = posX
        self.lastPosY = posY

        # Direction
        #self.vectDir = vectDirecteur  # on suppose qu'au début le robot est dirigé vers le haut
        self.theta = 0  # angle en degré

        # Roues du robot
        self.roue_gauche = Roue(rayon_roue, vmax_ang)
        self.roue_droite = Roue(rayon_roue, vmax_ang)

        # Capteur du robot
        self.capteur = Capteur(Vecteur(self.vectDir.x, self.vectDir.y/abs(self.vectDir.y)))

    # Propriété pour l'attribut posX
    @property
    def posX(self):
        return self._posX

    @posX.setter
    def posX(self, value):
        self._posX = value

    # Propriété pour l'attribut posY
    @property
    def posY(self):
        return self._posY

    @posY.setter
    def posY(self, value):
        self._posY = value

    # Propriété pour l'attribut theta
    @property
    def theta(self):
        return self._theta

    @theta.setter
    def theta(self, value):
        self._theta = value

    @property
    def coins(self):
        """ Renvoie les coord des 4 coins du robot 

        :returns: list[float]
        """
        u_x = self.vectDir.rotation(90).multiplication(self.width/2)
        u_y = self.vectDir.multiplication(self.length/2)

        OA = u_x.multiplication(-1).soustraction(u_y)
        OB = u_x.multiplication(-1).add(u_y)
        OC = u_x.add(u_y)
        OD = u_x.soustraction(u_y)

        x1, y1 = self.posX + OA.x , self.posY + OA.y
        x2, y2 = self.posX + OB.x , self.posY + OB.y
        x3, y3 = self.posX + OC.x , self.posY + OC.y
        x4, y4 = self.posX + OD.x , self.posY + OD.y

        return [x1, y1, x2, y2, x3, y3, x4, y4]

    @property
    def curr_pos(self) -> tuple[float, float]:
        """Renvoie la position actuelle du robot.

        :returns: Renvoie les coordonnées du robot (tuple).
        """
        return (self.posX, self.posY)

    @property
    def last_pos(self) -> tuple[float, float]:
        """Renvoie l'ancienne position du robot.

        :returns: Renvoie l'avant-dernière coordonnée du robot (tuple).
        """
        return (self.lastPosX, self.lastPosY)
    
    def vitesse(self):
        """Donne la vitesse du robot
        
        """
        #print(math.fabs(self.roue_gauche.vitesse_angulaire-self.roue_droite.vitesse_angulaire))
        return (self.roue_droite.rayon /2)* (self.roue_gauche.vitesse_angulaire-self.roue_droite.vitesse_angulaire)
    
    @property
    def vitesse_angulaire(self):
        """ Donne la vitesse angulaire du robot en fonction des vitesses angulaires des roues

        :returns: Renvoie la vitesse angulaire du robot
        """
        return (self.roue_droite.rayon /self.length)* ((self.roue_droite.vitesse_angulaire-self.roue_gauche.vitesse_angulaire))
    
    def move_dOM(self, dOM_x: float, dOM_y: float, dOM_theta = 0.):
        """ Robot avance d'un petit pas

        :param dOM: Vecteur de deplacement pour un dt.
        """
        self.lastPosX, self.lastPosY = self.posX, self.posY
        self.posX, self.posY = self.posX + dOM_x, self.posY + dOM_y
        self.theta = (self.theta + math.degrees(dOM_theta))%360
        self.vectDir = self.vectDir.rotation(math.degrees(dOM_theta))


class Capteur:
    def __init__(self, vecteur: Vecteur):
        """Initialisation du capteur

        :param vecteur : Vecteur directeur envoyé
        :param vitesse : Vitesse du rayon
        :returns : Retourne une instance de la classe Capteur
        """
        # Vecteur directeur
        self._vecteur = vecteur
        # Seuil de collision
        self._seuil_collision = 2
        self._deg_max = 10

    @property
    def vecteur(self):
        """Propriété pour l'attribut vecteur"""
        return self._vecteur

    @property
    def seuil_collision(self):
        """Propriété pour l'attribut seuil_collision"""
        return self._seuil_collision

    @property
    def deg_max(self):
        """Propriété pour l'attribut deg_max"""
        return self._deg_max
