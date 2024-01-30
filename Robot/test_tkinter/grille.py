# @autors equipe HELMS

from Exceptions.borneException import *

# Bibliotheque de la couleur du print
from colorama import init, Fore 
init(autoreset=True) # initilisation pour couleur

#On admettra que la dimension de la grille est forcement plus grande que le robot
#Une grille peut contenir au moins un robot

class Grille:
  def __init__(self, maxX, maxY, echelle):
    """ double x double x double -> Grille
    Initialisation de l'environnement 
    maxX et maxY sont les dimensions reelles de l'environnement exprimees en m
    """

    self.echelle = echelle
    self.maxX = int(maxX) # self.maxX est la taille maximun en x  de la fenetre 
    self.maxY = int(maxY) # self.maxX est la taille maximun en y de la fenetre
    self.grille = [["0" for case in range(self.maxY)] for ligne in range(self.maxX)]

  def addRobot(self, robot, dimX, dimY):
    """ Robot -> None
    Ajouter le robot dans la grille 
    """
    for ligne in range(int(dimY)):
      for col in range(int(dimX)):
        self.grille[robot.posY+ligne][robot.posX+col] = "R" 

  def addObstacle(self, obstacle, posX, posY):
    """ Obstacle x double x double -> None
    Mise en place d'un obstacle 
    """
    ### A corriger plsu tard ###
    self.grille[posY][posX] = obstacle
  
  def inBorne(self, posX, posY):
    """ double x double -> bool
    Verifie la position (posX, posY) est dans la grille
    """
    return 0 <= posX < self.maxX and 0 <= posY < self.maxY

  def isEmptyCase(self, posX, posY):
    """ double x double -> bool
    Renvoie true si la case en (posX,posY) est vide, sinon false 
    Lever une exception si on sort de la grille
    """
    if self.inBorne(posX, posY):
      return self.grille[posY][posX] == "0"
    raise BorneException("On sort de la borne") 

  def viderCase(self, posX, posY):
    """
    Vider la case (x,y)
    Lever une exception si on sort de la grille
    """
    if self.inBorne(posX, posY):
      self.grille[posY][posX] = "0"
    raise BorneException("On sort de la borne") 
  
  def setCase(self,posX, posY, contenu):
    """double x double x str -> None
    Modifie la case (posX, posY) de la grille
    Lever une exception si on sort de la grille
    """
    if self.inBorne(posX, posY):
      self.grille[posY][posX] = contenu
    else :
      raise BorneException("On sort de la borne") 
  
  def affiche(self):
    """ -> str
    Affiche la grille avec ses contenus(obstacle, robot etc)
    """
    print("-"*self.maxX+2*"-")

    for ligne in self.grille:
      print("|", end='')
      for contenu in ligne:
        if contenu == "R" : # Afficher le robot en rouge
          print(Fore.RED + contenu, end='')
        else : 
          print(contenu, end='')
      print("|")

    print("-"*self.maxX+2*"-")
