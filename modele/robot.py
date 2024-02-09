# @authors Équipe HELMS
from .vecteur import Vecteur
import math
# Supposons que les robots sont en forme de rectangle/carré
# Supposons que la position du robot (x, y) correspond à l'extrémité en haut à gauche

class Roue:
    def __init__(self, rayon:float, vmax_ang:float):
        """Initialisation d'une roue

        :param rayon: Le rayon de la roue
        :returns: Retourne une instance de la classe Roue.
        """
        self.rayon = rayon #m
        self.vmax_ang = vmax_ang #rad/s
        self.vitesse_angulaire = 0.0 #rad/s


    def set_vitesse_angulaire(self, vitesse_angulaire: float):
        """Modifier la vitesse angulaire lors d'un virage 

        :param vitesse_angulaire: Nouvelle vitesse angulaire de la roue
        """
        self.vitesse_angulaire = min(vitesse_angulaire, self.vmax_ang)

class Capteur:
    def __init__(self, vecteur : Vecteur):
        """Initialisation du capteur

        :param vecteur : Vecteur directeur envoyé
        :param vitesse : Vitesse du rayon
        :returns : Retourne une instance de la classe Capteur
        """
        # Vecteur directeur
        self.vecteur = vecteur

    def rotation(self, angle):
        self.vecteur = self.vecteur.rotation(angle)

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
        self.capteur = Capteur(self.vectDir)

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
    
    def vitesse(self):
        """Donne la vitesse du robot
        
        """
        print(math.fabs(self.roue_gauche.vitesse_angulaire-self.roue_droite.vitesse_angulaire))
        return (self.roue_droite.rayon /2)* (self.roue_gauche.vitesse_angulaire-self.roue_droite.vitesse_angulaire)
    
    def getVitesse_angulaire(self):
        """ Donne la vitesse angulaire du robot en fonction des vitesses angulaires des roues

        :returns: Renvoie la vitesse angulaire du robot
        """
        return (self.roue_droite.rayon /self.length)* ((self.roue_droite.vitesse_angulaire-self.roue_gauche.vitesse_angulaire))
    
    def move_dOM(self, dOM_x, dOM_y, dOM_theta = 0):
        """ Robot avance d'un petit pas

        :param dOM: Vecteur de deplacement pour un dt.
        """
        self.lastPosX, self.lastPosY = self.posX, self.posY
        self.posX, self.posY = self.posX + dOM_x, self.posY + dOM_y
        self.theta = (self.theta + math.degrees(dOM_theta))%360
        self.vectDir = self.vectDir.rotation(math.degrees(dOM_theta))

class Go(): 
    def __init__(self, robot: Robot, distance : int, v_ang_d, v_ang_g, dt) -> None:
        """/!!\\ robot ne comprends pas distance negative
        
        :param robot: Le robot qui va faire le deplacement 
        :param distance: La distance que le robot doit parcourir (float) 
        :param v_ang_d: La vitesse angulaire de la roue droite du robot en rad/s 
        :param v_ang_g: La vitesse angulaire de la roue gauche du robot en rad/s 
        :param dt: Le fps
        """
        self.robot = robot
        self.distance = distance

        # Modifier les vitesses angulaire les roues
        self.robot.roue_droite.set_vitesse_angulaire(v_ang_d)  # Vitesse angulaire droite
        self.robot.roue_gauche.set_vitesse_angulaire(v_ang_g)  # Vitesse angulaire gauche

        self.v_ang_d, self.v_ang_g = v_ang_d, v_ang_g

        #compteur de distance deja parcouru
        self.parcouru = 0

        #Coordonnee de vecteur de deplacement 
        self.dOM_x = robot.vectDir.x*robot.vitesse()*dt #/robot.grille.echelle 
        self.dOM_y = robot.vectDir.y*robot.vitesse()*dt #/robot.grille.echelle 

        self.dOM = Vecteur(self.dOM_x, self.dOM_y)

        self.dt = dt
        print("x, y", robot.vectDir.x, robot.vectDir.y)
        print(self.distance, self.v_ang_d, self.v_ang_g, self.dOM_x, self.dOM_y)

    def stop(self):
        """ Savoir le parcour est fini ou non

        :return : Retourne vrai si on fini de parcourir la distance  
        """
        return self.parcouru > self.distance

    def step(self):
        """ Faire un deplacement de dOM 
        """
        #Incrémenter la distance parcourru
        self.parcouru += self.dOM.norme
        if self.stop(): return
        
        self.dOM_theta = 0
        #Bouger le robot d'un dOM
        if -self.v_ang_d != self.v_ang_g: #si veut tourner 
            self.dOM_theta = -self.robot.roue_droite.rayon*(self.v_ang_g+self.v_ang_d)/self.robot.length * self.dt
            self.dOM_x = self.robot.vectDir.x*self.robot.vitesse()*self.dt #/robot.grille.echelle 
            self.dOM_y = self.robot.vectDir.y*self.robot.vitesse()*self.dt #/robot.grille.echelle 

            self.dOM = Vecteur(self.dOM_x, self.dOM_y)

            print(self.dOM_theta)
        self.robot.move_dOM(self.dOM_x, self.dOM_y, self.dOM_theta)