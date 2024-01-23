# @autors equipe HELMS
from Robot_v2_no_fini import Robot 
from Exceptions.BorneException import BorneException

#On admettra que la dimension de la grille est forcement plus grande que le robot
#Une grille peut contenir au moins un robot

class Grille:
  def __init__(self, maxX, maxY):
    """ double x double -> Grille
    Initialisation de l'environnement 
    """
    self.maxX = maxX
    self.maxY = maxY
    self.grille = [["0" for case in range(self.maxX)] for ligne in range(self.maxY)]

  def addRobot(self, robot):
    """ Robot -> None
    Ajouter le robot dans la grille 
    """
    self.grille[robot.posY][robot.posX] = "R" 

  def addObstacle(self, obstacle, posX, posY):
    """ Obstacle x double x double -> None
    Mise en place d'un obstacle 
    """
    self.grille[posY][posX] = obstacle
  
  def isEmptyCase(self, posX, posY):
    """ double x double -> bool
    Renvoie true si la case en (posX,posY) est vide, sinon false 
    """
    if posX > self.maxX or posX < 0 or posY > self.maxY or posY < 0:
      raise BorneException("On sort de la borne") #lever une exception si on sort de la grille
    else :
      return self.grille[posY][posX] == "0"
    
  def viderCase(self, posX, posY):
    """ double x double -> None
    Vide la case (posX, posY) de la grille
    """
    if posX > self.maxX or posX < 0 or posY > self.maxY or posY < 0:
      #print() # supprimer cette ligne quand class BorneException sera finie
      raise BorneException("On sort de la borne") #lever une exception si on sort de la grille
    else :
      self.grille[posY][posX] = "0"
  
  def setCase(self,posX, posY, contenu):
    """double x double x str -> None
    Modifie la case (posX, posY) de la grille
    """
    if posX > self.maxX or posX < 0 or posY > self.maxY or posY < 0:
      print() # supprimer cette ligne quand class BorneException sera finie
      #raise BorneException("On sort de la borne") #lever une exception si on sort de la grille
    else :
      self.grille[posY][posX] = contenu
  
  

  def affiche(self):
    """ -> str
    Affiche la grille avec ses contenus(obstacle, robot etc)
    """
    print("-"*self.maxX+2*"-")

    for ligne in self.grille:
      print("|", end='')
      for contenu in ligne:
        print(contenu, end='')
      print("|")

    print("-"*self.maxX+2*"-")

