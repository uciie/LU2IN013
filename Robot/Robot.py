# @autors equipe HELMS
from Exceptions import BorneException


class Robot:
  def __init__(self, name, posX, posY, dimLength, dimWidth,grille):
    """ str x double x double x Grille-> Robot
    Precondition: dimLength % 2 = 1 and dimWidth % 2 = 1
    Initialisation du robot 
    """
    # Nom du robot
    self.name = name 

    #Position du robot
    self.posX = posX
    self.posY = posY

    #Dimention du robot
    self.length = dimLength 
    self.width = dimWidth

    #Composant du robot
    #self.roue_r = Roue("right") #Roue droite du robot
    #self.roue_l = Roue("left") #Roue left du robot

    #Environnement du robot
    self.grille = grille

    self.vitesse = 0.

    ## A IGNORER POUR L'INSTANT###
    #self.batteries = batteries
    #self.camera = camera
    #self.capteurD = capteurD
    #self.accelerometre = accelerometre
  
  def getPos(self):
    """-> Tuple(double, double)
    Renvoie la position actuelle du robot
    """
    return (self.posX,self.posY)
  
  def go(self, distance):
    """ double -> None
    Precondition : distance >= 0
    Avancer d'une distance
    """
    new_posY = self.posY - distance # Nvlle position apres une distance distance
    
    #Tant qu'il n'y a pas d'obstacle à la case suivante et qu'on n'est pas arrivée à la nvlle position
    while self.posY != new_posY:
      try :
        if self.grille.isEmptyCase(self.posX, self.posY - 1):
          self.grille.viderCase(self.posX, self.posY) 
          self.posY -= 1
          self.grille.setCase(self.posX,self.posY, "R")
        else :
          break
      except IndexError as e :
        print("Mur touché")
        break
  
      

  def back(self, distance):
    """
    Reculer d'une distance
    """
    self.posY -= distance 

  def turnLeft(self, distance):
    """
    Tourner à gauche d'une distance 
    """

  def turnRight(self, distance):
    """
    Tourner à droite d'une distance 
    """
  
  def goToPos(self, posX, posY):
    """
    Se deplacer à la position (x,y) 
    """
