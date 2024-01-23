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
    for i in range(self.posX, self.largeur):
      for y in range(self.posY, self.longueur):
        (self.grille).addObstacle(1, i, y)
      (self.grille).addObstacle(1,i,y)
  
  def removeObstacle(self):
    for i in range(self.posX, self.largeur):
      for y in range(self.posY, self.longueur):
        (self.grille).viderCase()
      (self.grille).viderCase()
  