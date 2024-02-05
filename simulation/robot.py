# @authors Équipe HELMS
from .vecteur import Vecteur
import math
# Supposons que les robots sont en forme de rectangle/carré
# Supposons que la position du robot (x, y) correspond à l'extrémité en haut à gauche

class Roue:
    def __init__(self, rayon:float):
        """Initialisation d'une roue

        :param rayon: Le rayon de la roue
        :returns: Retourne une instance de la classe Roue.
        """
        self.rayon = rayon #m
        self.vitesse_angulaire = 0.0 #rad/s

    def set_vitesse_angulaire(self, vitesse_angulaire: float):
        """Modifier la vitesse angulaire lors d'un virage 

        :param vitesse_angulaire: Nouvelle vitesse angulaire de la roue
        """
        self.vitesse_angulaire = vitesse_angulaire


class Robot:
    def __init__(self, name: str, posX: float, posY: float, dimLength: float, dimWidth: float, vectDir : Vecteur, rayon_roue, color: str):
        """Initialisation du robot.

        :param name: Nom du robot (str).
        :param posX: Coordonnée x du robot (float).
        :param posY: Coordonnée y du robot (float).
        :param vectDir: Vecteur directeur du robot (Vecteur).
        :param dimLength: Longueur de la pièce en mètres (float).
        :param dimWidth: Largeur de la pièce en mètres (float).
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

        self.vectDir = vectDir

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

        # Vitesse
        self.vitesse = 5.0  # m/s

        self.roue_gauche = Roue(rayon_roue)
        self.roue_droite = Roue(rayon_roue)

    def getCurrPos(self) -> tuple[float, float]:
        """Renvoie la position actuelle du robot.

        :returns: Renvoie les coordonnées du robot (tuple).
        """
        return (self.posX, self.posY)

    def getLastPos(self) -> tuple[float, float]:
        """Renvoie l'ancienne position du robot.

        :returns: Renvoie l'avant-dernière coordonnée du robot (tuple).
        """
        return (self.lastPosX, self.lastPosY)
    
    def getVitesse_angulaire(self):
        """ Donne la vitesse angulaire du robot en fonction des vitesses angulaires des roues

        :returns: Renvoie la vitesse angulaire du robot
        """
        return (self.roue_droite.rayon /self.length)* (math.fabs(self.roue_droite.vitesse_angulaire-self.roue_gauche.vitesse_angulaire))
    
    def move_dOM(self, dOM_x, dOM_y, dOM_theta = 0):
        """ Robot avance d'un petit pas

        :param dOM: Vecteur de deplacement pour un dt.
        """
        self.lastPosX, self.lastPosY = self.posX, self.posY
        self.posX, self.posY = self.posX + dOM_x, self.posY + dOM_y
        self.theta = (self.theta + math.degrees(dOM_theta))%360
        self.vectDir = self.vectDir.rotation(math.degrees(dOM_theta))
