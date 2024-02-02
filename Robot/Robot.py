# @authors Équipe HELMS

# Supposons que les robots sont en forme de rectangle/carré
# Supposons que la position du robot (x, y) correspond à l'extrémité en haut à gauche

# FPS
dt = 1 / 30

class Robot:
    def __init__(self, name: str, posX: float, posY: float, dimLength: float, dimWidth: float, color: str):
        """Initialisation du robot.

        :param name: Nom du robot (str).
        :param posX: Coordonnée x du robot (float).
        :param posY: Coordonnée y du robot (float).
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

        # Dimension du robot sur la fenêtre
        self.length = dimLength  # /self.grille.echelle
        self.width = dimWidth  # /self.grille.echelle

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
