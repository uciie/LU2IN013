from .robot.robot_mere import Robot_mere 
from .vecteur import Vecteur
from .obstacle import Obstacle

class Arene(): 
    def __init__(self, name: str, maxX: int, maxY: int, echelle: float):
        """ Initisalisation d'une Arene 
        
        :param name: Nom de l'Arene
        :param maxX: La longeur maximale de l'Arene
        :param maxY: La largeur maximale de l'Arene
        :param echelle: L'echelle entre le plan et le IRLs
        """
        self.name = name
        self.maxX = maxX
        self.maxY = maxY
        self.echelle = echelle
        
        # robot dans l'Arene
        self.robot = None

        # listed'obstacle dans l'Arene
        self.liste_Obstacles = []

        self.color = "white"
    
    def inArene(self, posX: float, posY: float):
        """ Verifie si la position (posX, posY) est dans l'arène

        :param posX: Coordonnee en x 
        :param posY: Coordonnee en y
        :retruns bool: Renvoie true si (x,y) est dans l'arène, sinon false
        """
        return 0 <= posX < self.maxX and 0 <= posY < self.maxY
    
    def addRobot(self, robot: Robot_mere ):
        """ Ajouter un robot dans l'arene 
        
        """
        if not self.robot: 
            self.robot = robot
            self.robot.arene = self
    
    def addObstacle(self, obstacle:Obstacle):
        """Ajouter un obstacle dans l'arène

        """
        self.liste_Obstacles.append(obstacle)


    def isObstacle(self, posX: float, posY: float):
        """ Renvoie vrai si (posX, posY) fait partie d'un obstacle
    
        :param posX: Coordonnée en x
        :param posY: Coordonnée en y
        :return: bool
        """
        for obstacle in self.liste_Obstacles:
            Lcoins = obstacle.coins
            if (Lcoins[4] <= posX <= Lcoins[0]) and (Lcoins[1] <= posY <= Lcoins[5]):
                return True 
        return False
    
    def raytracing(self, robot: Robot_mere): 
        """ Renvoie la distance entre l'osbtacle et le capteur
        :param robot: Le robot
        :return : la distance en float 
        """
        #rayon du capteur capteur du robot 
        rayon = robot.capteur.vecteur

        #position à verifier 
        new_x, new_y= robot.posX + robot.vectDir.x*robot.width/2 + rayon.x, robot.posY + robot.vectDir.y*robot.length/2 + rayon.y

        # Verifier chaque pas de rayon 
        while self.inArene(new_x, new_y) and not self.isObstacle(new_x, new_y) :
            new_x += rayon.x
            new_y += rayon.y
        new_x -= rayon.x 
        new_y -= rayon.y
        
        #renvoie la norme, ie la distance 
        return Vecteur(robot.posX + robot.vectDir.x*robot.width/2 - new_x, robot.posY + robot.vectDir.y*robot.length/2  - new_y).norme
    
