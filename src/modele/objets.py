import math
import numpy as np
from abc import ABC, abstractmethod

from .utilitaire import Vecteur, project

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
    def vitesse_angulaire(self, value: float):
        """Modifie la vitesse angulaire de la roue, en s'assurant qu'elle ne dépasse pas la vitesse maximale.

        :param value: Nouvelle vitesse angulaire de la roue.
        """
        if value < -self.vmax_ang:
            self._vitesse_angulaire = -self.vmax_ang
        elif value > self.vmax_ang:
            self._vitesse_angulaire = self.vmax_ang
        else:
            self._vitesse_angulaire = value

class SimuRobot:
    """Classe qui permet de creer un robot"""

    def __init__(self, name: str, pos_x: float, pos_y: float, dim_length: float, dim_width: float, rayon_roue: int,
                 vmax_ang: float, color: str):
        """Initialisation du robot.

        :param name: Nom du robot (str).
        :param pos_x: Coordonnée x du robot (float).
        :param pos_y: Coordonnée y du robot (float).
        :param dim_length: Longueur de la pièce en mètres (float).
        :param dim_width: Largeur de la pièce en mètres (float).
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
        self._color = color  # couleur du robot

        self.vectDir = Vecteur(0, -1)  # vectDir

        # Dimension du robot sur la fenêtre
        self.length = dim_length  # /self.grille.echelle
        self.width = dim_width  # /self.grille.echelle

        # Initialisation de la position du robot
        self._pos_x = pos_x
        self._pos_y = pos_y

        # Ancienne position du robot
        # Initialise l'ancienne position à la position actuelle
        self._last_pos_x = pos_x
        self._last_pos_y = pos_y

        # Direction
        self._theta = 0.  # angle en degré
        # Ancien angle
        self._last_theta = 0.  # angle en degré

        # Activation du tracage du parcours
        self._tracer_parcours = None

        # Roues du robot
        self.roue_gauche = Roue(rayon_roue, vmax_ang)
        self.roue_droite = Roue(rayon_roue, vmax_ang)

    @property
    def tracer_parcours(self) -> bool:
        """Savoir si le tracer est active ou non"""
        return self._tracer_parcours

    def activer_tracer_parcours(self, valeur: bool):
        """Activer ou désactiver le traçage du parcours du robot.

        :param valeur: True pour activer le traçage, False pour le désactiver"""
        self._tracer_parcours = valeur

    # Propriété pour l'attribut pos_x
    @property
    def pos_x(self) -> float:
        """Getter Position en x du robot
        :return: Position en x du robot"""
        return self._pos_x

    @pos_x.setter
    def pos_x(self, value):
        """Setter Position en x du robot
        :param value: Nouvelle position en x du robot"""
        self._pos_x = value

    # Propriété pour l'attribut pos_y
    @property
    def pos_y(self) -> float:
        """Getter Position en y du robot
        :return: Position en y du robot"""
        return self._pos_y

    @pos_y.setter
    def pos_y(self, value: float):
        """Setter Position en y du robot
        :param value: Nouvelle position en y du robot"""
        self._pos_y = value

    @property
    def last_pos_x(self) -> float:
        """Getter de la derniere position en x du robot
        :return: derniere position en x du robot """
        return self._last_pos_x

    @last_pos_x.setter
    def last_pos_x(self, value: float):
        """Setter de la derniere position en x du robot
        :param value: Nouvelle de la derniere position en """
        self._last_pos_x = value

    @property
    def last_pos_y(self) -> float:
        """Getter de la derniere position en y du robot
        :return: derniere position en y du robot"""
        return self._last_pos_y

    @last_pos_y.setter
    def last_pos_y(self, value: float):
        """Setter de la derniere position en y
        :param value: Nouvelle de la derniere position en"""
        self._last_pos_y = value

    # Propriété pour l'attribut theta
    @property
    def theta(self) -> float:
        """getter du theta du robot
        :return: theta du robot"""
        return self._theta

    @property
    def last_theta(self) -> float:
        """Le dernier theta du robot
        :return: Le dernier theta du robot"""
        return self._last_theta

    @last_theta.setter
    def last_theta(self, value):
        """Setter du dernier theta du robot
        :param value: nouveau dernier theta """
        self._last_theta = value

    @property
    def curr_pos(self) -> tuple[float, float]:
        """Renvoie la position actuelle du robot.

        :returns: Renvoie les coordonnées du robot (tuple).
        """
        return self.pos_x, self.pos_y

    @property
    def last_pos(self) -> tuple[float, float]:
        """Renvoie l'ancienne position du robot.

        :returns: Renvoie l'avant-dernière coordonnée du robot (tuple).
        """
        return self.last_pos_x, self.last_pos_y

    @property
    def color(self) -> str:
        return self._color

    @color.setter
    def color(self, color: str):
        """Setter de la couleur de l'obstacle """
        self._color = color

    @property
    def coins(self):
        """ Renvoyer les coordonnees des 4 coins du robot

        :returns: list[float]
        """
        u_x = self.vectDir.rotation(90).multiplication(self.width / 2)
        u_y = self.vectDir.multiplication(self.length / 2)

        oa = u_x.multiplication(-1).soustraction(u_y)
        ob = u_x.multiplication(-1).add(u_y)
        oc = u_x.add(u_y)
        od = u_x.soustraction(u_y)

        x1, y1 = self.pos_x + oa.x, self.pos_y + oa.y
        x2, y2 = self.pos_x + ob.x, self.pos_y + ob.y
        x3, y3 = self.pos_x + oc.x, self.pos_y + oc.y
        x4, y4 = self.pos_x + od.x, self.pos_y + od.y

        return [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]

    def test_crash(self, max_x: int, max_y: int)-> bool:
        """ Tester si le robot entre ds un mur

        :param max_x: La largeur de l'arene
        :param max_y: La hauteur de l'arene
        :return bool: True si hors de l'arene, False sinon
        """
        # Verifier si les coins du robot sont à l'interieur de l'arene
        for coin_x, coin_y in self.coins:
            if coin_x < 0 or coin_x >= max_x or coin_y < 0 or coin_y >= max_y:
                return True
        return False

    @property
    def vitesse(self) -> float:
        """Donne la vitesse du robot

        :returns float: Renvoie la vitesse du robot
        """
        return (self.roue_droite.rayon / 2) * (self.roue_gauche.vitesse_angulaire + self.roue_droite.vitesse_angulaire)

    @property
    def vitesse_angulaire(self) -> float:
        """ Donne la vitesse angulaire du robot en fonction des vitesses angulaires des roues

        :returns: Renvoie la vitesse angulaire du robot
        """
        return (self.roue_droite.rayon / self.length) * (
                self.roue_droite.vitesse_angulaire - self.roue_gauche.vitesse_angulaire)

    def actualiser(self, dt: float) -> None:
        """ Actualise le robot selon le dt ecoule

        :param dt: Temps ecoule
        :return: None
        """
        self._last_pos_x = self._pos_x
        self._last_pos_y = self._pos_y
        self._last_theta = self._theta

        # Màj des coordonnees du robot selon les vitesses angulaires des roues
        x = (self.roue_droite.vitesse_angulaire + self.roue_gauche.vitesse_angulaire) * math.cos(
            self.vectDir.angle) * self.roue_droite.rayon / 2 * dt
        y = (self.roue_droite.vitesse_angulaire + self.roue_gauche.vitesse_angulaire) * math.sin(
            self.vectDir.angle) * self.roue_droite.rayon / 2 * dt
        theta = self.roue_droite.rayon * (
                self.roue_droite.vitesse_angulaire - self.roue_gauche.vitesse_angulaire) / self.length * dt
        self._pos_x += x
        self._pos_y += y
        self._theta += math.degrees(theta)  # Incrémentation de l'angle sans ajustement
        # Ajustement de l'angle entre -360 et 360 degrés
        if self._theta > 360:
            self._theta -= 360
        elif self._theta < -360:
            self._theta += 360
        self.vectDir = self.vectDir.rotation(math.degrees(theta))

    def info(self) -> str:
        """ afficher les informations du robot
        :return str: informations du robot
        """
        info_str = ""
        info_str += f"Position: ({self.pos_x}, {self.pos_y})\n"
        info_str += f"Vitesse roue droite: {self.roue_droite.vitesse_angulaire}\n"
        info_str += f"Vitesse roue gauche: {self.roue_gauche.vitesse_angulaire}\n"
        return info_str


########################
class Obstacle(ABC):
    """Classe de l'obstacle'"""

    def __init__(self, pos_x: float, pos_y: float, color: str):
        """ Initialise un obstacle

        :param pos_x: Coordonnée X de l'obstacle (float)
        :param pos_y: Coordonnée y de l'obstacle (float)
        :param color: Couleur de l'obstacle
        """
        # Coordonnées du centre de l'obstacle
        self._pos_x = pos_x
        self._pos_y = pos_y

        # couleur de l'obstacle
        self._color = color

    @property
    def color(self) -> str:
        return self._color

    @color.setter
    def color(self, color: str):
        """Setter de la couleur de l'obstacle 
        :param color: Nouvelle couleur de l'obstacle"""
        self._color = color

    @property
    def pos_x(self) -> float:
        """ Propriété pour l'attribut pos_x 
        :return: float"""
        return self._pos_x

    @property
    def pos_y(self) -> float:
        """ Propriété pour l'attribut pos_y 
        :return: float"""
        return self._pos_y

    @abstractmethod
    def test_collision(self, robot):
        """ Méthode abstraite pour tester la collision entre l'obstacle et un robot """
        pass

    @property
    @abstractmethod
    def coins(self):
        """ Renvoie les coordonnées des 4 coins de l'obstacle """
        pass


#############
class Arene:
    """ Classe de l'Arene"""

    def __init__(self, name: str, max_x: int, max_y: int, echelle: float):
        """ Initisalisation d'une Arene

        :param name: Nom de l'Arene
        :param max_x: La longeur maximale de l'Arene
        :param max_y: La largeur maximale de l'Arene
        :param echelle: L'echelle entre le plan et le IRLs
        """
        self.name = name
        self.max_x = max_x
        self.max_y = max_y
        self.echelle = echelle

        # listed'obstacle dans l'Arene
        self.liste_Obstacles = []

        self.color = "white"

    def in_arene(self, pos_x: float, pos_y: float) -> bool:
        """ Verifie si la position (pos_x, pos_y) est dans la grille

        :param pos_x: Coordonnee en x
        :param pos_y: Coordonnee en y
        :retrun bool: Renvoie true si (x,y) est dans la grille, sinon false
        """
        return 0 <= pos_x < self.max_x and 0 <= pos_y < self.max_y

    def add_obstacle(self, obstacle: Obstacle):
        """Ajouter un obstacle dans l'arène

        :param obstacle: Obstacle à ajouter
        """
        self.liste_Obstacles.append(obstacle)

    def is_obstacle(self, pos_x: float, pos_y: float):
        """ Renvoie vrai si (pos_x, pos_y) fait partie d'un obstacle

        :param pos_x: Coordonnée en x
        :param pos_y: Coordonnée en y
        :return: bool
        """
        for obstacle in self.liste_Obstacles:
            l_coins = obstacle.coins
            if (l_coins[4] <= pos_x <= l_coins[0]) and (l_coins[1] <= pos_y <= l_coins[5]):
                return True
        return False


class ObstacleRectangle(Obstacle):
    def __init__(self, pos_x: float, pos_y: float, coin1: Vecteur, coin2: Vecteur, color: str):
        """ Initialise un obstacle rectangulaire

        :param pos_x: Coordonnée X de l'obstacle (float)
        :param pos_y: Coordonnée y de l'obstacle (float)
        :param coin1: Côté haut
        :param coin2: Côté bas
        :param color: Couleur de l'obstacle
        """
        super().__init__(pos_x, pos_y, color)

        # Vecteurs directeurs de l'obstacle
        self._coin1 = coin1
        self._coin2 = coin2

    @property
    def coin1(self) -> Vecteur:
        """ Propriété pour l'attribut v1 """
        return self._coin1

    @property
    def coin2(self) -> Vecteur:
        """ Propriété pour l'attribut v2 """
        return self._coin2

    @property
    def coins(self):
        """ Renvoie les coordonnées des 4 coins de l'obstacle """
        x1, y1 = self._pos_x + self._coin1.x / 2, self._pos_y - self._coin2.y / 2
        x2, y2 = self._pos_x + self._coin1.x / 2, self._pos_y + self._coin2.y / 2
        x3, y3 = self._pos_x - self._coin1.x / 2, self._pos_y + self._coin2.y / 2
        x4, y4 = self._pos_x - self._coin1.x / 2, self._pos_y - self._coin2.y / 2

        return [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]

    def test_collision(self, robot: SimuRobot):
        """Tester si l'obstacle est en collision avec le robot.

        :param robot: Robot sur lequel on teste la collision
        :return: True si collision, sinon False
        """
        vect_dir_normal = robot.vectDir.rotation(90)
        axes = [[1, 0], [0, 1], [robot.vectDir.x, robot.vectDir.y], [vect_dir_normal.x, vect_dir_normal.y]]
        cpt = 0
        for axe in axes:
            self_interval = project(axe, self.coins)
            point_interval = project(axe, robot.coins)
            if self_interval[0] <= point_interval[1] and point_interval[0] <= self_interval[1]:
                cpt += 1
        return cpt == 4

    def in_obstacle(self, pos_x: float, pos_y: float)-> bool:
        """Tester si le point (x, y) fait portie de l'obstacle

        :param pos_x: x position
        :param pos_y: y position
        :return: True si collision, sinon False
        """
        axes = [[1, 0], [0, 1]]
        cpt = 0
        for axe in axes:
            self_interval = project(axe, self.coins)
            point_interval = project(axe, [(pos_x, pos_y)])
            if self_interval[0] <= point_interval[1] and point_interval[0] <= self_interval[1]:
                cpt += 1
        return cpt == 2


class Balise(ObstacleRectangle):
    def __init__(self, pos_x: float, pos_y: float, color2d: str):
        """Initialisation d'une balise

        :param pos_x: Coordonnée X de la balise (float)
        :param pos_y: Coordonnée y de la balise (float)
        :param color: Couleur de la balise
        """
        super().__init__(pos_x, pos_y, color2d)
    
    
        # plage de couleurs pour la reconnaissance d'image (balise)
        self.plages_couleurs = {
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