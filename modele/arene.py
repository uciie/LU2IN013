from .robot import Robot
    
class Arene(): 
    def __init__(self, name: str, maxX: int, maxY: int, echelle: float, color: str):
        """ Initisalisation d'une Arene 
        
        :param name: Nom de l'Arene
        :param maxX: La longeur maximale de l'Arene
        :param maxY: La largeur maximale de l'Arene
        :param echelle: L'echelle entre le plan et le IRL
        :param color: La couleur de l'Arene
        :param
        :param
        """
        self.name = name
        self.maxX = maxX
        self.maxY = maxY
        self.echelle = echelle
        
        # robot dans l'Arene
        self.robot = None

        # Ensemble d'obstacle dans l'Arene
        self.ensObstacles = set()

        self.color = color
    
    @property
    def name(self):
        return self.__name

    @property
    def maxX(self):
        return self.__maxX
    
    @property
    def maxY(self):
        return self.__maxY
    
    @property
    def echelle(self):
        return self.__echelle
    
    @property
    def robot(self):
        return self.__robot

    def inArene(self, posX, posY):
        """ Verifie si la position (posX, posY) est dans la grille

        :param grille: La fenetre 
        :param posX: Coordonnee en x 
        :param posY: Coordonnee en y
        :retruns bool: Renvoie true si (x,y) est dans la grille, sinon false
        """
        return 0 <= posX < self.width and 0 <= posY < self.height
    
    def addRobot(self, robot:Robot ):
        """ Ajouter un robot dans l'arene 
        
        """
        self.robot = robot