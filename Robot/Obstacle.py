# @autors equipe HELMS
from Grille import Grille
class Obstacle:
  def __init__(self, posX, posY, longueur, largeur, grille):
    for i in range(posX, largeur):
      for y in range(posY, longueur):
        grille.addObstacle(1, i, y)
      grille.addObstacle(1,i,y)