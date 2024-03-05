from .robot_mere import Roue, Capteur, Robot_mere
from .robot2I013 import Robot2IN013
from ..vecteur import Vecteur
import math


class Robot(Robot_mere):
    def __init__(self, name: str, posX: float, posY: float, dimLength: float, dimWidth: float, rayon_roue:int , vmax_ang : float, color: str):
        """Initialisation du robot.

        :param name: Nom du robot (str).
        :param posX: Coordonnée x du robot (float).
        :param posY: Coordonnée y du robot (float).
        :param dimLength: Longueur de la pièce en mètres (float).
        :param dimWidth: Largeur de la pièce en mètres (float).
        :param rayon_roue: Rayon des roues du robot (int)
        :param vmax_ang : Vitesse maximale angulaire du robot 
        :param color: Couleur du robot (str).
        :returns: Retourne une instance de la classe Robot.
        """
        super().__init__()

        # Nom du robot
        self.name = name

        # Fenêtre graphique
        # Identifiants des objets graphiques dans l'interface
        self.rect_id = None  # Identifiant du rectangle
        self.arrow_id = None  # Identifiant de la flèche
        self.line_id = None  # Identifiant de sa tracabilite
        self.color = color  # couleur du robot

        self.vectDir = Vecteur(0, -1)  # vectDir

        # Dimension du robot sur la fenêtre
        self.length = dimLength  # /self.grille.echelle
        self.width = dimWidth  # /self.grille.echelle

        # Initialisation de la position du robot
        self._posX = posX
        self._posY = posY

        # Ancienne position du robot
        # Initialise l'ancienne position à la position actuelle
        self._lastPosX = posX
        self._lastPosY = posY

        # Direction
        self._theta = 0  # angle en degré

        # Roues du robot
        self.roue_gauche = Roue(rayon_roue, vmax_ang)
        self.roue_droite = Roue(rayon_roue, vmax_ang)

        # Capteur du robot
        self.capteur = Capteur(Vecteur(self.vectDir.x, self.vectDir.y / abs(self.vectDir.y)))

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
    
    @property
    def lastPosX(self) -> float:
        return self._lastPosX

    @lastPosX.setter
    def lastPosX(self, value: float):
        self._lastPosX = value

    @posY.setter
    def posY(self, value):
        self._posY = value

    @property
    def lastPosY(self) -> float:
        return self._lastPosY

    @lastPosY.setter
    def lastPosY(self, value: float):
        self._lastPosY = value

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
    
    @property
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
    
    def move_dOM(self, dOM_x: float, dOM_y: float, dOM_theta: float = 0.):
        """ Robot avance d'un petit pas

        :param dOM_x: Déplacement en x pour un dt
        :param dOM_y: Déplacement en y pour un dt
        :param dOM_theta: Angle pour un dt (float)
        """
        self.lastPosX, self.lastPosY = self.posX, self.posY
        self.posX, self.posY = self.posX + dOM_x, self.posY + dOM_y
        self.theta = (self.theta + math.degrees(dOM_theta)) % 360
        self.vectDir = self.vectDir.rotation(math.degrees(dOM_theta))

    def calcul_dOM(self, dt: float): 
        """ Calcul les dOM pour lezs utiliser lors de appel de go_dOM

        :param robot: Le robot qui va faire le deplacement 
        :param dt: Le fps
        """
        dOM_theta = -self.roue_droite.rayon*(self.roue_droite.vitesse_angulaire+self.roue_gauche.vitesse_angulaire)/self.length * dt
        dOM_x = self.vectDir.x*self.vitesse*dt #/robot.grille.echelle 
        dOM_y = self.vectDir.y*self.vitesse*dt #/robot.grille.echelle 

        return dOM_theta, dOM_x, dOM_y
    
    def set_vitesse_roue(self, v_ang_roue_d: float, v_ang_roue_g: float):
        """ Modifier la vitesse des roues droite et gauche 

        :param v_ang_roue_d: vitesse roue droite 
        :param v_ang_roue_g: vitesse roue gauche
        """
        self.roue_droite.vitesse_angulaire = v_ang_roue_d
        self.roue_gauche.vitesse_angulaire = v_ang_roue_g
    
    def stop(self):
        """ Arreter le robot 
        """
        self.set_vitesse_roue(0,0)
    
    def step(self, dOM_x: float, dOM_y: float, dt: float):
        """ Faire un petit pas
        :param dOM_x: Déplacement en x pour un dt
        :param dOM_y: Déplacement en y pour un dt
        :param dt: 
        :return vecteur:
        """
        dOM_theta = 0
        #Bouger le robot d'un dOM
        if -self.roue_droite.vitesse_angulaire != self.roue_gauche.vitesse_angulaire: #si veut tourner 
            #Calcul des dOM
            print(self.calcul_dOM(dt))
            dOM_theta, dOM_x, dOM_y = self.calcul_dOM(dt)
            #print(self.dOM_theta)
        self.move_dOM(dOM_x, dOM_y, dOM_theta)
        return Vecteur(dOM_x, dOM_y)

class Adaptateur_robot(Robot_mere):
    def __init__(self, robot_irl: Robot2IN013):
        """ Adaptateur du robot irl
        """
        super().__init__()
        self._robot_irl = robot_irl

    def set_vitesse_roue(self, v_ang_roue_d: float, v_ang_roue_g: float):
        self._robot_irl.set_motor_dps("roue_droite", math.degrees(v_ang_roue_d))
        self._robot_irl.set_motor_dps("roue_gauche", math.degrees(v_ang_roue_g))

    def stop(self): 
        """ Arrete le robot irl
        """
        self._robot_irl.stop 
    

