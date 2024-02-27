from .robot import Robot
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

        # Ensemble d'obstacle dans l'Arene
        self.ensObstacles = set()

        self.color = "white"
    
    def inArene(self, posX, posY):
        """ Verifie si la position (posX, posY) est dans la grille

        :param grille: La fenetre 
        :param posX: Coordonnee en x 
        :param posY: Coordonnee en y
        :retruns bool: Renvoie true si (x,y) est dans la grille, sinon false
        """
        return 0 <= posX < self.maxX and 0 <= posY < self.maxY
    
    def addRobot(self, robot:Robot ):
        """ Ajouter un robot dans l'arene 
        
        """
        if not self.robot: 
            self.robot = robot
            self.robot.arene = self
    
    def addObstacle(self, obstacle:Obstacle):
        """Ajouter un obstacle dans l'arène

        """
        self.ensObstacles.add(obstacle)


    def isObstacle(self, posX, posY):
        """ Renvoie vrai si (posX, posY) fait partie d'un obstacle
    
        :param posX: 
        :param posY:
        :return: bool
        """
        for obstacle in self.ensObstacles:
            Lcoins = obstacle.getCoins()
            if ( posX >= Lcoins[0] and posX <= Lcoins[2]) and (posY >= Lcoins[1] and posY <= Lcoins[5]):
                return True 
        return False
    
    def raytracing(self, robot: Robot): 
        """ Renvoie la distance entre l'osbtacle et le capteur

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
    
