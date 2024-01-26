# @autors equipe HELMS

from Exceptions.borneException import *
from vecteur import *
from robot import *

import sys
import pygame 


# Supposons que les robot sont en forme de rectangle/carre
# Supposons que la position du robot (x,y) correspond a l'extremite en haut à gauche

class Robot:
  def __init__(self, name, posX, posY, dimLength, dimWidth, grille, vectDirecteur, fenetre, blanc, rouge ):
    """ str x double x double x Grille x Vecteur -> Robot
    Precondition: dimLength % 2 = 1 and dimWidth % 2 = 1
    Initialisation du robot 
    """
    # Nom du robot
    self.name = name 

    # Fenetre graphique 
    self.fenetre = fenetre
    self.blanc= blanc # Grille
    self.rouge = rouge # Robot

    #Environnement du robot
    self.grille = grille

    #Dimention du robot
    self.length = dimLength 
    self.width = dimWidth

    #Position du robot
    # Tentative de positionnement du robot
    while True:
      try:
        assez_espace = True
        for ligne in range(self.length):
          for col in range(self.width):
            #print((posX+ligne, posY+col))
            if not self.grille.isEmptyCase(posX+ligne, posY+col):
              raise PosNonValideException #leve une exception car la case est occupee
        self.posX = posX
        self.posY = posY
        break # Sortir de la boucle si la position n'est valide
      
      except BorneException or PosNonValideException or IndexError as e:
        # Si une exception est levée, redemander les coordonnées
        posX = int(input("Entrez une nouvelle coordonnée X : "))
        posY = int(input("Entrez une nouvelle coordonnée Y : "))
    
    #Ajout du robot dans la grille
    self.grille.addRobot(self, self.length, self.width)

    #Ancienne position du robot
    #Initilise l'ancienne position à la position actuelle
    self.lastPosX = posX 
    self.lastPosY = posY

    # Direction
    self.vectDir = Vecteur(0,1)#on suppose qu'au debut le robot est dirigé vers le haut 
    self.angle = 0 # angle en degre
    
    # Vitesse
    self.vitesse = 5.0 # m/s

    # Calculer le temps écoulé depuis la dernière mise à jour
    self.dt = pygame.time.Clock().tick(30) / 1000.0  # convertir en secondes

    #Composant du robot
    #self.roue_r = Roue("right") #Roue droite du robot
    #self.roue_l = Roue("left") #Roue left du robot

    ## A IGNORER POUR L'INSTANT###
    #self.batteries = batteries
    #self.camera = camera
    #self.capteurD = capteurD
    #self.accelerometre = accelerometre
  
  def getCurrPos(self):
    """-> Tuple(double, double)
    Renvoie la position actuelle du robot
    """
    return (self.posX,self.posY)
  
  def getLastPos(self):
    """-> Tuple(double, double)
    Renvoie la position actuelle du robot
    """
    return (self.lastPosX,self.lastPosY)
  
  def update(self, new_x, new_y):
    """ -> None
    Mettre à jour la grille et la position du robot
    """
    #mise à jour les positions
    self.lastPosX = self.posX
    self.lastPosY = self.posY

    for ligne in range(self.length):
      for col in range(self.width):
        self.grille.viderCase(self.lastPosX, self.lastPosY)

    self.posX = new_x
    self.posY = new_y

    #mise à jour de la grille
    self.grille.viderCase(self.lastPosX, self.lastPosY) 
    self.grille.setCase(self.posX,self.posY, "R")
      
  def go(self, angle, distance, vitesse):
    """ str x double x double -> None
    Avancer d'une distance d'un certain degre, l'unite de la distance est en m, ce dernier doit etre convertie à l'echelle
    On sait que la frequence d'image  = 30 images/s, on peut determiner le dt 
    Etape 1 : 
      - on effectue le rotation (on estime qu'elle est instantennee)
    Etape 2:
      - trouver le vecteur de deplacement dOM
    Etape 3:
      - deplacer le robot de dOM
    Etape 4:
      - faire une boucle jusqua avoir fait la distance attendue 

    """
    print(self.vectDir.x,self.vectDir.y)
    # on modifie le directeur directeur
    self.vectDir = self.vectDir.rotation(angle)
    print(self.vectDir.x,self.vectDir.y)

    # on modifie la vitesse du robot
    self.vitesse = vitesse

    # compteur de distance parcourrue
    cpt_dis = 0

    #Coordonnee de vecteur de deplacement 
    d_OM_x = self.vectDir.x*vitesse * self.dt*self.grille.echelle 
    d_OM_y = self.vectDir.y*vitesse * self.dt *self.grille.echelle 
    d_OM = Vecteur(d_OM_x, d_OM_y)
    
    #tant qu'on n'a pas fini de parcourrir tte la distance on effectue un d_OM
    while cpt_dis < distance :
      new_x = self.posX + d_OM.x
      new_y = self.posY + d_OM.y

      # Mettre à jour l'ancienne position du robot
      self.lastPosX = self.posX
      self.lastPosY = self.posY

      # Mettre à jour de la position du robot
      self.posX += d_OM.x
      self.posY += d_OM.y
      cpt_dis += d_OM.norme
      #print(cpt_dis)

      #### Mise à jour de la fenetre ####
      # Effacer l'écran
      self.fenetre.fill(self.blanc)

      # Dessiner le robot
      pygame.draw.rect(self.fenetre, self.rouge, (self.posX, self.posY, self.length, self.width))

      # Mettre à jour l'affichage
      pygame.display.flip()


  def goToPos(self, posX, posY):
    """
    Se deplacer à la position (x,y) 
    """

