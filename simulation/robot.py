# @authors Équipe HELMS
from .vecteur import Vecteur
# Supposons que les robots sont en forme de rectangle/carré
# Supposons que la position du robot (x, y) correspond à l'extrémité en haut à gauche

# FPS
dt = 1 / 30

class Robot:
    def __init__(self, name: str, posX: float, posY: float, dimLength: float, dimWidth: float, vectDir : Vecteur, color: str):
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
        self.rect = None  # le robot
        self.arrow = None  # vecteur directeur
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
        self.angle = 0  # angle en degré

        # Vitesse
        self.vitesse = 5.0  # m/s

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
    
    def move_dOM(self, dOM_x, dOM_y):
        """ Robot avance d'un petit pas

        :param dOM: Vecteur de deplacement pour un dt.
        """
        self.lastPosX, self.lastPosY = self.posX, self.posY
        self.posX, self.posY = self.posX + dOM_x, self.posY + dOM_y

class Roue:
    def __init__(self, nom : str , vecteur : Vecteur , vitesse : float):
        """Initialisation de la roue"""

        # Vitesse de la roue
        self.nom = nom
        self.vecteur = vecteur
        self.vitesse = vitesse
    
    def avancer(self):
        """Fait avancer la roue"""
        print("La roue ",nom," tourne à ",vitesse,"RPM, suivant le vecteur directeur ", vecteur)