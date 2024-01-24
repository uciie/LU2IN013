# @autors equipe HELMS

# affichage en couleur 
from colorama import init, Fore 
init(autoreset=True) # initilisation pour couleur

from Robot_v2 import Robot 
from Exceptions.BorneException import BorneException

#On admettra que la dimension de la grille est forcement plus grande que le robot
#Une grille peut contenir au moins un robot

class Grille:
  def __init__(self, maxX, maxY, echelle):
    """ double x double x double -> Grille
    Initialisation de l'environnement 
    """
    self.echelle = echelle
    self.maxX = maxX
    self.maxY = maxY
    self.grille = [["0" for case in range(self.maxY)] for ligne in range(self.maxX)]

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
  
  def inBorne(self, posX, posY):
    """ double x double -> bool
    Verifie la position (posX, posY) est dans la grille
    """
    return 0 <= posX < self.maxX and 0 <= posY < self.maxY

  def isEmptyCase(self, posX, posY):
    """ double x double -> bool
    Renvoie true si la case en (posX,posY) est vide, sinon false 
    """
    if self.inBorne(posX, posY):
      return self.grille[posY][posX] == "0"
    else : 
      raise BorneException("On sort de la borne") #lever une exception si on sort de la grille

  def viderCase(self, posX, posY):
    """ double x double -> None
    Vide la case (posX, posY) de la grille
    """
    if self.inBorne(posX, posY):
      self.grille[posY][posX] = "0"
    else : 
      raise BorneException("On sort de la borne") #lever une exception si on sort de la grille
  
  def setCase(self,posX, posY, contenu):
    """double x double x str -> None
    Modifie la case (posX, posY) de la grille par contenu 
    """
    if self.inBorne(posX, posY):
      self.grille[posY][posX] = contenu
    else :
      raise BorneException("On sort de la borne") #lever une exception si on sort de la grille
  
  def affiche(self):
    """ -> str
    Affiche la grille avec ses contenus(obstacle, robot etc)
    """
    print("-"*self.maxX+2*"-")

    for ligne in self.grille:
      print("|", end='')
      for contenu in ligne:
        if contenu == "R" : 
          print(Fore.RED + contenu, end='')
        else : 
          print(contenu, end='')
      print("|")

    print("-"*self.maxX+2*"-")