# @autors equipe HELMS
from Grille import Grille
class Obstacle:
  def __init__(self, posX, posY, longueur, largeur, grille):
    self.posX = posX
    self.posY = posY
    self.longueur = longueur
    self.largeur = largeur
    self.grille = grille
  
  def addObstacle(self):
    for i in range(posX, largeur):
      for y in range(posY, longueur):
        grille.addObstacle(1, i, y)
      grille.addObstacle(1,i,y)
  
  def removeObstacle(self):
    for i in range(posX, largeur):
      for y in range(posY, longueur):
        grille.viderCase()
      grille.viderCase()
  