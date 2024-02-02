# @autors equipe HELMS

from exceptions import *

# Bibliotheque de la couleur du print
from colorama import init, Fore 
init(autoreset=True) # initilisation pour couleur

#On admettra que la dimension de la grille est forcement plus grande que le robot
#Une grille peut contenir au moins un robot

class Grille:
  def __init__(self, maxX, maxY, echelle):
    """Initialisation de l'environnement 
    :param maxX: longueur x de la grille 
    :param maxY: largueur y de la grille 
    :param echelle: correspondance entre case de la grille et taille reelle
    :returns: retourne la grille generer
    """

    self.echelle = echelle
    self.maxX = int(maxX) # self.maxX est la taille maximun en x  de la fenetre 
    self.maxY = int(maxY) # self.maxX est la taille maximun en y de la fenetre
    self.grille = [["0" for case in range(self.maxY)] for ligne in range(self.maxX)]

  def affiche(self):
    """Affiche la grille avec ses contenus(obstacle, robot etc)
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
