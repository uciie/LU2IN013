# @autors equipe HELMS
from Exceptions.borneException import BorneException
from vecteur import Vecteur
from grille_v2_no_fini import Grille
import sys
import pygame 

# Supposons que les robot sont en forme de rectangle/carre
# Supposons que la position du robot (x,y) correspond a l'extremite en haut à gauche

class Robot:
  def __init__(self, name, posX, posY, dimLength, dimWidth, grille, vectDirecteur):
    """ str x double x double x Grille x Vecteur -> Robot
    Precondition: dimLength % 2 = 1 and dimWidth % 2 = 1
    Initialisation du robot 
    """
    # Nom du robot
    self.name = name 

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
        #print(f"Erreur : {e}")

        # Si une exception est levée, redemander les coordonnées
        posX = int(input("Entrez une nouvelle coordonnée X : "))
        posY = int(input("Entrez une nouvelle coordonnée Y : "))
    
    self.grille.addRobot(self, self.length, self.width)

    #Ancienne position du robot
    #Initilise l'ancienne position à la position actuelle
    self.lastPosX = posX 
    self.lastPosY = posY

    # Direction
    self.vectDir = Vecteur(1,1)#on suppose qu'au debut le robot est dirigé vers le haut 
    self.angle = 0 # angle en degre

    #Composant du robot
    #self.roue_r = Roue("right") #Roue droite du robot
    #self.roue_l = Roue("left") #Roue left du robot

    self.vitesse = 5.0 # m/s

    ## A IGNORER POUR L'INSTANT###
    #self.batteries = batteries
    #self.camera = camera
    #self.capteurD = capteurD
    #self.accelerometre = accelerometre
    
  def go2(self, angle, distance, vitesse, fenetre, blanc, rouge):
    """ Avancer d'une distance en utilisant Pygame """
    # on modifie le vecteur directeur
    self.vectDir = self.vectDir.rotation(angle)
    # on modifie la vitesse du robot
    self.vitesse = vitesse

    # Initialiser le temps écoulé
    clock = pygame.time.Clock()

    # Boucle d'événements Pygame
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Calculer le temps écoulé depuis la dernière mise à jour
        dt = clock.tick(30) / 1000.0  # convertir en secondes

        # Calculer la distance parcourue pendant cette période
        distance_parcourue = self.vitesse * dt

        # Mettre à jour la position du robot
        self.posX += self.vectDir.x * distance_parcourue
        self.posY += self.vectDir.y * distance_parcourue

        # Effacer l'écran
        fenetre.fill(blanc)

        # Dessiner le robot
        pygame.draw.rect(fenetre, rouge, (self.posX, self.posY, self.length, self.width))

        # Mettre à jour l'affichage
        pygame.display.flip()

        # Vérifier si la distance totale a été parcourue
        if distance_parcourue >= distance:
            break  # Sortir de la boucle si la distance totale est parcourue


